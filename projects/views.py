import json
from random import choice
import traceback
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.template import loader, RequestContext
import sys
from projects.forms import ProjectForm, TaskForm

from projects.models import Task, User, Project, PersonInProject, File

# TODO add 'user_project_list' for all users in public profile
# TODO rss ?

# NOTE: 'user' in templates is a reserved keyword

"""
date format:
	https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
forms:
	https://docs.djangoproject.com/en/dev/topics/forms/modelforms/
	https://docs.djangoproject.com/en/dev/ref/forms/validation/
ajax:
	http://stackoverflow.com/questions/11647715/how-to-submit-form-without-refreshing-page-using-django-ajax-jquery
	http://lethain.com/two-faced-django-part-5-jquery-ajax/
	http://stackoverflow.com/questions/20306981/how-do-i-integrate-ajax-with-django-applications
	http://racingtadpole.com/blog/django-ajax-and-jquery/
models:
	http://www.djangobook.com/en/2.0/chapter05.html
	http://www.djangobook.com/en/2.0/chapter10.html
"""

def get_current_user():
	return choice(User.objects.all())

def get_context(tmplContext):
	user = get_current_user()
	context = {
		'currentUser': user,
		'user_id': user.id,
		'task_count': len(Task.objects.all()),
	}
	# concat
	return dict(list(context.items()) + list(tmplContext.items()))


#
# projects
#

def project(request, id):
	try:
		p = Project.objects.get(id=id)
	except Project.DoesNotExist:
		return HttpResponseNotFound('<h1>Project not found</h1>')

	# TODO fetching all relations by hand ?
	p.tasks = Task.objects.filter(projectId=id)
	p.people__ = PersonInProject.objects.filter(projectId=id)
	p.people = [uid.userId for uid in p.people__]
	p.files = File.objects.filter(projectId=id)

	template = loader.get_template('project_read.html')
	context = RequestContext(request, get_context({
		'project': p,
		'data_page_type': 'projects',
		'can_edit': True
	}))
	return HttpResponse(template.render(context))

def project_edit(request, id):
	try:
		usr = get_current_user()
		p = Project.objects.get(id=id)
		# TODO fetching all relations by hand ?
		p.tasks = Task.objects.filter(projectId=id)
		p.people__ = PersonInProject.objects.filter(projectId=id)
		p.people = [uid.userId for uid in p.people__ if uid.userId.id != usr.id] # TODO remove current user :)
		p.files = File.objects.filter(projectId=id)
	except Project.DoesNotExist:
		return HttpResponseNotFound('<h1>Project not found</h1>')

	if request.method == "POST" and request.is_ajax():
		ok, opt = __project_edit(p, request)
		if ok:
			return HttpResponse(json.dumps({"status":"OK"}))
		else:
			errors_fields = dict()
			if opt:
				errors_fields["fields"] = opt
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		template = loader.get_template('project_write.html')
		context = RequestContext(request, get_context({
			'project': p,
			'data_page_type': 'projects'
		}))
		return HttpResponse(template.render(context))

def project_create(request):
	if request.method == "POST" and request.is_ajax():
		print(request.POST)
		form = ProjectForm(request.POST)
		if form.is_valid():
			usr = get_current_user()
			p = Project(name=form.cleaned_data['name'],
						complete=form.cleaned_data['complete'],
						description=form.cleaned_data['description'],
						createdBy=usr)
			p.save(True,False)
			# TODO add creator as admin !
			pip = PersonInProject(projectId=p,
					  	userId=usr,
						role=PersonInProject.PERSON_ROLE[1][0],
						createdBy=usr)
			pip.save(True,False)
			return HttpResponse(json.dumps({"status":"OK","id":p.id}))
		else:
			errors_fields = dict()
			if form.errors:
				errors_fields["fields"] = list(form.errors.keys())
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		template = loader.get_template('project_write.html')
		context = RequestContext(request, get_context({
			'new_project': True,
			'data_page_type': 'projects'
		}))
		return HttpResponse(template.render(context))

def project_list(request):
	template = loader.get_template('project_list.html')
	context = RequestContext(request, get_context({
		'projects': Project.objects.all(),
		'data_page_type': 'projects'
	}))
	return HttpResponse(template.render(context))

def user_project_list(request, id):
	return project_list(request)


#
# tasks
#
# TODO utilize task status

def task(request, id):
	template = loader.get_template('task_read.html')
	try:
		task = Task.objects.get(id=id)
	except Task.DoesNotExist:
		return HttpResponseNotFound('<h1>Task not found</h1>')

	context = RequestContext(request, get_context({
		'task': task,
		'canAddComment': False,
		'data_page_type': 'tasks',
		'taskTypes': Task.TASK_TYPES,
		'can_edit': True
	}))
	return HttpResponse(template.render(context))

def task_edit(request, id, back_url=""):
	try:
		task = Task.objects.get(id=id)
	except Task.DoesNotExist:
		return HttpResponseNotFound('<h1>Task not found</h1>')

	if request.method == "POST" and request.is_ajax():
		ok, opt = __task_edit( task, request)
		if ok:
			return HttpResponse(json.dumps({"status":"OK"}))
		else:
			errors_fields = dict()
			if opt:
				errors_fields["fields"] = opt
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		template = loader.get_template('task_write.html')

		context = RequestContext(request, get_context({
			'task': task,
			'taskTypes': Task.TASK_TYPES,
			'data_page_type': 'tasks',
			'people_to_assign': User.objects.all()
		}))
		return HttpResponse(template.render(context))

def task_create(request, project_id):
	try:
		project = Project.objects.get(id=project_id)
	except Project.DoesNotExist:
		return HttpResponseNotFound('<h1>Project not found</h1>')

	if request.method == "POST" and request.is_ajax():
		print(request.POST)
		form = TaskForm(request.POST)
		if form.is_valid():
			p = Task(projectId=project,
				title=form.cleaned_data['title'],
				type=form.cleaned_data['type'],
				deadline=form.cleaned_data['deadline'],
				description=form.cleaned_data['description'],
				createdBy=get_current_user())
			p.save(True,False)
			__assign_person(p, request)
			return HttpResponse(json.dumps({"status":"OK","id":p.id}))
		else:
			errors_fields = dict()
			if form.errors:
				errors_fields["fields"] = list(form.errors.keys())
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		template = loader.get_template('task_write.html')
		context = RequestContext(request, get_context({
			'new_task': True,
			'taskTypes': Task.TASK_TYPES,
			'data_page_type': 'tasks',
			'project_id': project_id,
			'people_to_assign': User.objects.all()
		}))
		return HttpResponse(template.render(context))

def user_tasks_list(request, id):
	template = loader.get_template('task_list.html')
	context = RequestContext(request, get_context({
		'tasks': Task.objects.all(),
		'data_page_type': 'tasks'
	}))
	return HttpResponse(template.render(context))


#
# __utils
#

def __project_edit(project, request):
	# print(request.POST)
	tasksToRemove = request.POST["tasksToRemove"]
	peopleToRemove = request.POST["peopleToRemove"]
	filesToRemove = request.POST["filesToRemove"]
	form = ProjectForm(request.POST)
	if form.is_valid():
		project.name = form.cleaned_data['name']
		project.complete = form.cleaned_data['complete']
		project.description = form.cleaned_data['description']
		project.createdBy = get_current_user()
		project.save(False,True)
		return True, {}
	else:
		return False, list(form.errors.keys()) if form.errors else None

def __task_edit( task, request):
	print(request.POST)
	# filesToRemove = request.POST["filesToRemove"]
	# personResponsibleID = request.POST["personResponsibleId"]
	form = TaskForm(request.POST)
	if form.is_valid():
		task.title = form.cleaned_data['title']
		task.type = form.cleaned_data['type']
		task.deadline = form.cleaned_data['deadline']
		task.description = form.cleaned_data['description']
		task.createdBy = get_current_user()
		task.save(False,True)
		__assign_person(task,request)
		return True, {}
	else:
		return False, list(form.errors.keys()) if form.errors else None

def __assign_person( task, request):
	key = "personResponsibleId"
	if key in request.POST:
		try:
			personId = int(request.POST[key])
			print(">>> assign person: "+str(personId))
			if personId > 0:
				user = User.objects.get(id=personId)
				task.personResponsible = user
			else:
				task.personResponsible = None
			task.save(False,True)
			print(">>> OK")
			return
		except Exception as e:
			# print(">>> Exception" + e.)
			traceback.print_exc(file=sys.stdout)
			pass
	print(">>> NO person")