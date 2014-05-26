from django.forms import ModelForm
from projects.models import Project, Task

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'complete', 'description']
	# created
	# createdBy
	# modifiedDate

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['projectId', 'personResponsible', 'title',
			'type', 'deadline', 'description'] # 'status',
	# created
	# createdBy
	# modifiedDate
