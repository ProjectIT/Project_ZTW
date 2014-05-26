import json
from random import choice
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader, RequestContext
from projects.forms import ProjectForm, TaskForm

from projects.models import Task, User, Project
from projects.stubs import create_stub_user, __createExampleTask

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

"""

def get_current_user():
	return choice(User.objects.all())

def get_context(tmplContext):
	user = get_current_user()
	context = {
		'currentUser': user,
		'user_id': user.id,
		'task_count': 2,
	}
	# concat
	return dict(list(context.items()) + list(tmplContext.items()))


#
# projects
#

def project(request, id):
	# TODO handle errors
	p = Project.objects.filter(id=id)[0]
	template = loader.get_template('project_read.html')
	context = RequestContext(request, get_context({
		'project': p,
		'data_page_type': 'projects',
		'can_edit': True
	}))
	return HttpResponse(template.render(context))

def project_edit(request, id):
	if request.method == "POST" and request.is_ajax():
		ok, opt = __project_edit(request,id)
		if ok:
			return HttpResponse(json.dumps({"status":"OK"}))
		else:
			errors_fields = dict()
			if opt:
				errors_fields["fields"] = opt
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		p = Project.objects.filter(id=id)[0]
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
			p = Project(name=form.cleaned_data['name'],
						complete=form.cleaned_data['complete'],
						description=form.cleaned_data['description'],
						createdBy=get_current_user())
			p.save(True,False)
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
	task = __createExampleTask()

	context = RequestContext(request, get_context({
		'task': task,
		'canAddComment': False,
		'data_page_type': 'tasks',
		'taskTypes': Task.TASK_TYPES,
		'can_edit': True
	}))
	return HttpResponse(template.render(context))

def task_edit(request, id, back_url=""):
	if request.method == "POST" and request.is_ajax():
		ok, opt = __task_edit(request,id)
		if ok:
			return HttpResponse(json.dumps(opt))
		else:
			errors_fields = dict()
			if opt:
				errors_fields["fields"] = opt
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		# TODO back_url - we need to acknowledge that sometimes we want to go back to the projectWrite, not to taskRead
		template = loader.get_template('task_write.html')
		task = __createExampleTask()
		pplAssignable = [create_stub_user() for _ in range(7)]

		context = RequestContext(request, get_context({
			'task': task,
			'taskTypes': Task.TASK_TYPES,
			'data_page_type': 'tasks',
			'people_to_assign': pplAssignable
		}))
		return HttpResponse(template.render(context))

def task_create(request, project_id):
	if request.method == "POST" and request.is_ajax():
		print(request.POST)
		form = TaskForm(request.POST)
		if form.is_valid():
			return HttpResponse(json.dumps({"status":"OK","id":13}))
		else:
			errors_fields = dict()
			if form.errors:
				errors_fields["fields"] = list(form.errors.keys())
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")
	else:
		template = loader.get_template('task_write.html')
		pplAssignable = [create_stub_user() for _ in range(7)]
		context = RequestContext(request, get_context({
			'new_task': True,
			'taskTypes': Task.TASK_TYPES,
			'data_page_type': 'tasks',
			'project_id': project_id,
			'people_to_assign': pplAssignable
		}))
		return HttpResponse(template.render(context))

def user_tasks_list(request, id):
	ts = [__createExampleTask() for _ in range(7)]

	template = loader.get_template('task_list.html')
	context = RequestContext(request, get_context({
		'tasks': ts,
		'data_page_type': 'tasks'
	}))
	return HttpResponse(template.render(context))


#
# __utils
#

def __project_edit(request, id):
	# print(request.POST)
	tasksToRemove = request.POST["tasksToRemove"]
	peopleToRemove = request.POST["peopleToRemove"]
	filesToRemove = request.POST["filesToRemove"]
	form = ProjectForm(request.POST)
	if form.is_valid():
		p = Project.objects.filter(id=id)[0]
		p.name = form.cleaned_data['name']
		p.complete = form.cleaned_data['complete']
		p.description = form.cleaned_data['description']
		p.createdBy = get_current_user()
		p.save(False,True)
		return True, {}
	else:
		return False, list(form.errors.keys()) if form.errors else None

def __task_edit(request, id):
	print(request.POST)
	filesToRemove = request.POST["filesToRemove"]
	personResponsibleID = request.POST["personResponsibleId"]
	form = TaskForm(request.POST)
	if form.is_valid():
		return True, {"status":"OK"}
	else:
		return False, list(form.errors.keys()) if form.errors else None