import json
from django.db import transaction

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.template import loader, RequestContext

from projects.forms import ProjectForm
from projects.models import Task, User, Project, PersonInProject, File, UserProfile


# TODO add 'user_project_list' for all users in public profile

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

def getTasksAssignedToCurrentUser(request):
	usr = request.user
	return Task.objects.filter(personResponsible=usr)

def get_context(tmplContext, request):
	user = request.user
	context = {
		'currentUser': user,
		'user_id': user.id,
		'task_count': len(getTasksAssignedToCurrentUser(request)),
	}
	# concat
	return dict(list(context.items()) + list(tmplContext.items()))

def getUserProfilesForUsers( users):
	return UserProfile.objects.filter(user__in=users)

def canViewProject( request, project):
	usr = request.user
	try:
		a=PersonInProject.objects.get(projectId=project, userId=usr)
		print(a)
	except PersonInProject.DoesNotExist:
		return False
	return True


#
# projects
#

def project(request, id):
	try:
		p = Project.objects.get(id=id)
	except Project.DoesNotExist:
		return HttpResponseNotFound('<h1>Project not found</h1>')
	if not canViewProject(request,p):
		hr = HttpResponse("<h1>You are not a part of this project</h1>")
		hr.status_code = 412
		return hr

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
	}, request))
	return HttpResponse(template.render(context))

def project_edit(request, id):
	try:
		usr = request.user
		p = Project.objects.get(id=id)
		# TODO fetching all relations by hand ?
		p.tasks = Task.objects.filter(projectId=id)
		p.people__ = PersonInProject.objects.filter(projectId=id)
		p.people = [uid.userId for uid in p.people__ if uid.userId.id != usr.id] # remove current user
		p.files = File.objects.filter(projectId=id)
	except Project.DoesNotExist:
		return HttpResponseNotFound('<h1>Project not found</h1>')

	if not canViewProject(request,p):
		hr = HttpResponse("<h1>You are not a part of this project</h1>")
		hr.status_code = 412
		return hr

	if request.method == "POST" and request.is_ajax():
		ok, opt = __project_edit(p, request)
		if ok:
			return HttpResponse(json.dumps({"status":"OK"}))
		else:
			errors_fields = dict()
			if opt:
				errors_fields["fields"] = opt
			return HttpResponseBadRequest(json.dumps(errors_fields), content_type="application/json")

	elif request.method == "DELETE" and request.is_ajax():
		p.delete()
		return HttpResponse(json.dumps({"success":True}))

	else:
		template = loader.get_template('project_write.html')
		context = RequestContext(request, get_context({
			'project': p,
			'data_page_type': 'projects'
		}, request))
		return HttpResponse(template.render(context))

def project_create(request):
	usr = request.user
	if request.method == "POST" and request.is_ajax():
		print(request.POST)
		form = ProjectForm(request.POST)
		if form.is_valid():
			p = Project(name=form.cleaned_data['name'],
						complete=form.cleaned_data['complete'],
						description=form.cleaned_data['description'],
						createdBy=usr)
			p.save(True,False)
			# add creator as admin !
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
		}, request))
		return HttpResponse(template.render(context))

def project_list(request):
	usr = request.user
	template = loader.get_template('project_list.html')
	myProjects = PersonInProject.objects.filter(userId=usr)
	myProjects = [pip.projectId for pip in myProjects]
	context = RequestContext(request, get_context({
		'projects': myProjects,
		'data_page_type': 'projects'
	}, request))
	return HttpResponse(template.render(context))

def user_project_list(request, id):
	return project_list(request)

def users_for_project_search(request, project_id):
	if request.method != "POST" or not request.is_ajax():
		return HttpResponseNotFound('<h1>Page not found</h1>')
	try:
		p = Project.objects.get(id=project_id)
		if not canViewProject(request,p):
			hr = HttpResponse("<h1>You are not a part of this project</h1>")
			hr.status_code = 412
			return hr

		people__ = PersonInProject.objects.filter(projectId=project_id)
		peopleAlreadyIn = [uid.userId.id for uid in people__]
		print("exclude: "+str(peopleAlreadyIn))

		name = request.POST["name"]
		last_name = request.POST["last-name"]
		user_name = request.POST["user-name"]
		token = request.POST["search-token"]
		print( name + "|" + last_name + "|" + user_name)

		# query
		result = User.objects\
			.filter(first_name__contains=name)\
			.filter(last_name__contains=last_name)\
			.filter(username__contains=user_name)\
			.exclude(id__in=peopleAlreadyIn)
		result = getUserProfilesForUsers(result)
		print("found"+str(len(result)))
		if len(result) < 20:
			arr = []
			for r in result:
				arr.append({
					"id":r.user.id,
					"name":r.user.username,
					"last_name":r.user.last_name,
					"avatar_path":r.avatarPath
				})
			return HttpResponse(json.dumps({"search-token":token,"status":True,"data":arr }))
		else:
			return HttpResponse(json.dumps({"search-token":token,"status":False,"found-count":len(result)}))
	except Project.DoesNotExist:
		return HttpResponseNotFound('<h1>Project not found</h1>')
	hr = HttpResponse({"status":"error"})
	hr.status_code = 412
	return hr

#
# __utils
#

def __project_edit(project, request):
	usr = request.user
	# print(request.POST)
	tasksToRemove = request.POST["tasksToRemove"]
	peopleToRemove = request.POST["peopleToRemove"]
	filesToRemove = request.POST["filesToRemove"]
	peopleToAdd = request.POST["peopleToAdd"]

	form = ProjectForm(request.POST)
	if form.is_valid():
		project.name = form.cleaned_data['name']
		project.complete = form.cleaned_data['complete']
		project.description = form.cleaned_data['description']
		project.createdBy =request.user
		project.save(False,True)
		# remove composites
		try:
			# TODO
			tasksToRemove = json.loads(tasksToRemove)
			peopleToRemove = json.loads(peopleToRemove)
			peopleToAdd = json.loads(peopleToAdd)
			with transaction.atomic():
				Task.objects.filter(projectId=project).filter(id__in=tasksToRemove).delete()
				PersonInProject.objects.filter(projectId=project).filter(userId__in=peopleToRemove).delete()
				# 	File.objects.filter(projectId=project).filter(id__in=filesToRemove).delete()
				for userId in peopleToAdd:
					print(">>"+str(userId))
					u = User.objects.get(id=userId)
					if u:
						PersonInProject(projectId=project, userId=u, createdBy=usr).save()
		except (User.DoesNotExist,Exception) as e:
			print("Error modifying project's companion objects: "+ str(e))
		return True, {}
	else:
		return False, list(form.errors.keys()) if form.errors else None
