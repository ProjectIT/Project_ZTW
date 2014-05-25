from django.forms import ModelForm
from projects.models import Project

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'complete', 'description']
	# created
	# createdBy
	# modifiedDate
