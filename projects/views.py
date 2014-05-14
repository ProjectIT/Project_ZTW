from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader, RequestContext
from projects.models import Task
from projects.stubs import create_stub_project, create_stub_user, create_stub_task, create_stub_file, \
	create_stub_task_comment

# TODO add 'user_project_list' for all users in public profile

# NOTE: 'user' in templates is a reserved keyword

# date format:
#https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date

def __createExampleProject():
	# just for testing
	project_creator = create_stub_user()
	p = create_stub_project(project_creator)
	p.tasks = [create_stub_task(p, project_creator, create_stub_user()) for _ in range(4)]
	p.people = [create_stub_user() for _ in range(4)]
	p.files = [create_stub_file(project_creator,projectId=p) for _ in range(4)]
	return p

def __createExampleTask():
	# just for testing
	project_creator = create_stub_user()
	t = create_stub_task( __createExampleProject(), create_stub_user(),create_stub_user())
	t.files = [create_stub_file(project_creator,taskId=t) for _ in range(4)]
	t.comments = [ create_stub_task_comment(t,project_creator) for _ in range(4)]
	return t


def get_context( tmplContext):
	user=create_stub_user()
	context = {
		'currentUser':user,
		'user_id':user.id,
		'task_count':2,
	}
	# concat
	return dict(list(context.items()) + list(tmplContext.items()))


#
# projects
#
def project(request, id):
	p = __createExampleProject()

	template = loader.get_template('project_read.html')
	context = RequestContext(request,  get_context({
		'projectId': id,
		'project': p,
		'data_page_type':'projects'
	}))
	return HttpResponse(template.render(context))

def project_edit(request, id):
	p = __createExampleProject()

	template = loader.get_template('project_write.html')
	context = RequestContext(request,  get_context({
		'projectId': id,
		'project': p,
		'data_page_type':'projects'
	}))
	return HttpResponse(template.render(context))

def project_create(request):
	template = loader.get_template('project_write.html')
	context = RequestContext(request,  get_context({
		'new_project': True,
		'data_page_type':'projects'
	}))
	return HttpResponse(template.render(context))


def project_list(request):
	ps = [__createExampleProject() for _ in range(7)]

	template = loader.get_template('project_list.html')
	context = RequestContext(request, get_context({
		'projects':ps,
		'data_page_type':'projects'
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

	context = RequestContext(request,  get_context({
		'taskId': id,
		'task': task,
		'canAddComment':False,
		'data_page_type':'tasks',
		'taskTypes': Task.TASK_TYPES,
	}))
	return HttpResponse(template.render(context))

def task_edit(request, id, back_url=""):
	# TODO back_url - we need to acknowledge that sometimes we want to go back to the projectWrite, not to taskRead
	template = loader.get_template('task_write.html')
	task = __createExampleTask()

	context = RequestContext(request,  get_context({
		'taskId': id,
		'task': task,
		'taskTypes': Task.TASK_TYPES,
		'data_page_type':'tasks'
	}))
	return HttpResponse(template.render(context))

def task_create(request):
	template = loader.get_template('task_write.html')
	context = RequestContext(request,  get_context({
		'new_project': True,
		'taskTypes': Task.TASK_TYPES,
		'data_page_type':'tasks'
	}))
	return HttpResponse(template.render(context))

def user_tasks_list(request, id):
	ts = [__createExampleTask() for _ in range(7)]

	template = loader.get_template('task_list.html')
	context = RequestContext(request,  get_context({
		'tasks':ts,
		'data_page_type':'tasks'
	}))
	return HttpResponse(template.render(context))

