import json
import traceback
import sys

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.template import loader, RequestContext

from projects.forms import TaskForm
from projects.models import Task, User, Project, File, TaskComment, UserProfile


# TODO utilize task status
from projects.views import get_context, getTasksAssignedToCurrentUser

def task(request, id):
	template = loader.get_template('task_read.html')
	try:
		task = Task.objects.get(id=id)
		task.files = File.objects.filter(projectId=id)
		task.comments = TaskComment.objects.filter(taskId=id)
	except Task.DoesNotExist:
		return HttpResponseNotFound('<h1>Task not found</h1>')

	context = RequestContext(request, get_context({
		'task': task,
		'canAddComment': True,
		'data_page_type': 'tasks',
		'taskTypes': Task.TASK_TYPES,
		'can_edit': True
	}, request))
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
	elif request.method == "DELETE" and request.is_ajax():
		task.delete() #TODO check permissions
		return HttpResponse(json.dumps({"success":True}))
	else:
		template = loader.get_template('task_write.html')

		assginablePeople = UserProfile.objects.all() # TODO ( and check other 'alls')
		context = RequestContext(request, get_context({
			'task': task,
			'taskTypes': Task.TASK_TYPES,
			'data_page_type': 'tasks',
			'people_to_assign': assginablePeople
		}, request))
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
				createdBy = request.user)
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
		}, request))
		return HttpResponse(template.render(context))

def user_tasks_list(request, id):
	template = loader.get_template('task_list.html')
	myTasks = getTasksAssignedToCurrentUser(request)
	context = RequestContext(request, get_context({
		'tasks': myTasks,
		'data_page_type': 'tasks'
	}, request))
	return HttpResponse(template.render(context))

def task_comment(request, task_id):
	if request.method != "POST" or not request.is_ajax():
		return HttpResponseNotFound('<h1>Page not found</h1>')
	try:
		task = Task.objects.get(id=task_id)
		text = request.POST["new-comment-text"]
		if len(text)>0:
			tc = TaskComment(taskId=task,
					text=text,
					createdBy=request.user)
			tc.save( True, False)
			d = tc.created
			tcJson = {
				"id":tc.id,
				"text":tc.text,
				"created":[d.year,d.month,d.day],
				"createdBy":{
					"name":tc.createdBy.name,
					"lastName":tc.createdBy.lastName
				}
			}
			return HttpResponse(json.dumps({"status":"OK","data":tcJson}))
	except Task.DoesNotExist:
		return HttpResponseNotFound('<h1>Task not found</h1>')
	hr = HttpResponse({"status":"error"})
	hr.status_code = 412
	return hr

#
# __utils
#

def __task_edit( task, request):
	print(request.POST)
	filesToRemove = request.POST["filesToRemove"]
	# personResponsibleID = request.POST["personResponsibleId"]
	form = TaskForm(request.POST)
	if form.is_valid():
		task.title = form.cleaned_data['title']
		task.type = form.cleaned_data['type']
		task.deadline = form.cleaned_data['deadline']
		task.description = form.cleaned_data['description']
		task.createdBy = request.user
		task.save(False,True)
		__assign_person(task,request)
		# remove composites TODO not tested
		# File.objects.filter(taskId=task).filter(id__in=filesToRemove).delete()
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