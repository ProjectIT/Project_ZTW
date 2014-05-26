import os
from django.db import models

# ids:
# id = models.AutoField(primary_key=True)
# https://docs.djangoproject.com/en/dev/topics/db/models/#automatic-primary-key-fields

# foreign key docs:
# https://docs.djangoproject.com/en/1.6/topics/db/queries/#backwards-related-objects

class User(models.Model):
	# TODO reuse the Django table ?
	GENDERS = (
		('F','Female'),
		('M','Male')
	)
	name = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	email = models.EmailField()
	login = models.CharField(max_length=50, unique=True)
	password = models.CharField(max_length=50)
	gender = models.CharField(max_length=1, choices=GENDERS, default='F')
	birthdate = models.DateTimeField()
	registerDate = models.DateTimeField(auto_now_add=True, editable=False)
	modifiedDate = models.DateTimeField(auto_now=True, editable=False)
	lastLoginDate = models.DateTimeField() # used for f.e. activity stream etc.
	avatarPath = models.CharField(max_length=128, editable=False,default="stub_imgs/avatar2.jpg") # path to image file
	# ?description

class Project(models.Model):
	name = models.CharField(max_length=50,blank=False)
	complete = models.PositiveSmallIntegerField() # percent complete - from 0 to 100
	description = models.CharField(max_length=1024,blank=True)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	createdBy = models.ForeignKey(User, editable=False)
	modifiedDate = models.DateTimeField(auto_now=True, editable=False)

class Task(models.Model):
	TASK_TYPES = (
		('B','Bug'),
		('I','Improvement'),
		('F','New Feature'),
		('O','Other')
	)
	# TASK_PRIORITY = (
	# 	('B','Blocker'),
	# 	('C','Critical'),
	# 	('J','Major'),
	# 	('M','Minor'),
	# 	('T','Trivial'),
	# )

	# https://confluence.atlassian.com/display/JIRA/What+is+an+Issue
	TASK_STATUS = (
		('O','Open'),
		('P','In Progress'),
		('R','Resolved'),
		('C','Closed'),
		('D','Duplicate'),
		('X','Cannot Reproduce'),
	)

	projectId = models.ForeignKey(Project, null = True, blank=True, default = None) # TODO !!! PROJECT_ID CAN BE NULL !!!
	personResponsible = models.ForeignKey(User, related_name='task_person_responsible', null = True, blank=True, default = None)
	title = models.CharField(max_length=50,blank=False)
	type = models.CharField(max_length=1, choices=TASK_TYPES, default='T')
	# priority =models.CharField(max_length=1, choices=TASK_PRIORITY, default='M')
	# status = models.CharField(max_length=1, choices=TASK_STATUS, default='O')
	deadline = models.DateTimeField()
	description = models.CharField(max_length=1024,blank=False)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	createdBy = models.ForeignKey(User, editable=False, related_name='task_created_by')
	modified = models.DateTimeField(auto_now=True, editable=False)

class TaskComment(models.Model):
	taskId = models.ForeignKey(Task, editable=False)
	text = models.CharField(max_length=1024)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	createdBy = models.ForeignKey(User, editable=False)
	# TODO images ?

class File(models.Model):
	FILE_TYPE = (
		('D','Document'),
		('I','Image'),
		('S','Sound'),
		('O','Other')
	)

	taskId = models.ForeignKey(Task, editable=False, null = True)
	projectId = models.ForeignKey(Project, editable=False, null = True)
	type = models.CharField(max_length=1, choices=FILE_TYPE, default='O', editable=False)
	# https://docs.djangoproject.com/en/dev/ref/models/fields/#filefield
	# path = models.CharField(max_length=128, editable=False)
	# path = models.FileField(upload_to=os.path.join("projects", "attachments"))
	path = models.FileField(upload_to="projects/attachments")
	created = models.DateTimeField(auto_now_add=True, editable=False)
	createdBy = models.ForeignKey(User, editable=False)

class PersonInProject(models.Model):
	PERSON_ROLE = (
		('O','Observer'),
		('A','Admin'),
		('U','User')
	)

	projectId = models.ForeignKey(Project)
	userId = models.ForeignKey(User, related_name='person_in_project_user')
	role = models.CharField(max_length=1, choices=PERSON_ROLE, default='U')
	created = models.DateTimeField(auto_now_add=True, editable=False)
	createdBy = models.ForeignKey(User, editable=False, related_name='person_in_project_created_by')