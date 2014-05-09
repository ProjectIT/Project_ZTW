# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            name = 'User',
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),), ('name', models.CharField(max_length=50),), ('lastName', models.CharField(max_length=50),), ('email', models.EmailField(max_length=75),), ('login', models.CharField(unique=True, max_length=50),), ('password', models.CharField(max_length=50),), ('gender', models.CharField(choices=(('F', 'Female',), ('M', 'Male',),), max_length=1, default='F'),), ('birthdate', models.DateTimeField(),), ('registerDate', models.DateTimeField(auto_now_add=True),), ('modifiedDate', models.DateTimeField(auto_now=True),), ('lastLoginDate', models.DateTimeField(),)],
            options = {},
        ),
        migrations.CreateModel(
            name = 'Project',
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),), ('name', models.CharField(max_length=50),), ('complete', models.PositiveSmallIntegerField(),), ('description', models.CharField(max_length=1024),), ('created', models.DateTimeField(auto_now_add=True),), ('createdBy', models.ForeignKey(to_field='id', to='projects.User', editable=False),), ('modifiedDate', models.DateTimeField(auto_now=True),)],
            options = {},
        ),
        migrations.CreateModel(
            name = 'personInProject',
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),), ('projectId', models.ForeignKey(to_field='id', to='projects.Project'),), ('userId', models.ForeignKey(to_field='id', to='projects.User'),), ('role', models.CharField(choices=(('O', 'Observer',), ('A', 'Admin',), ('U', 'User',),), max_length=1, default='U'),), ('created', models.DateTimeField(auto_now_add=True),), ('createdBy', models.ForeignKey(to_field='id', to='projects.User', editable=False),)],
            options = {},
        ),
        migrations.CreateModel(
            name = 'Task',
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),), ('projectId', models.ForeignKey(to_field='id', to='projects.Project'),), ('personResponsible', models.ForeignKey(to_field='id', to='projects.User'),), ('title', models.CharField(max_length=50),), ('type', models.CharField(choices=(('B', 'Bug',), ('I', 'Improvement',), ('F', 'New Feature',), ('T', 'Task',), ('O', 'Other',),), max_length=1, default='T'),), ('status', models.CharField(choices=(('O', 'Open',), ('P', 'In Progress',), ('R', 'Resolved',), ('C', 'Closed',), ('D', 'Duplicate',), ('X', 'Cannot Reproduce',),), max_length=1, default='O'),), ('deadline', models.DateTimeField(),), ('description', models.CharField(max_length=1024),), ('created', models.DateTimeField(auto_now_add=True),), ('createdBy', models.ForeignKey(to_field='id', to='projects.User', editable=False),), ('modified', models.DateTimeField(auto_now=True),)],
            options = {},
        ),
        migrations.CreateModel(
            name = 'File',
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),), ('taskId', models.ForeignKey(to_field='id', to='projects.Task', editable=False),), ('projectId', models.ForeignKey(to_field='id', to='projects.Project', editable=False),), ('type', models.CharField(choices=(('D', 'Document',), ('I', 'Image',), ('S', 'Sound',), ('O', 'Other',),), editable=False, max_length=1, default='O'),), ('path', models.CharField(editable=False, max_length=128),), ('created', models.DateTimeField(auto_now_add=True),), ('createdBy', models.ForeignKey(to_field='id', to='projects.User', editable=False),)],
            options = {},
        ),
        migrations.CreateModel(
            name = 'TaskComment',
            bases = (models.Model,),
            fields = [('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),), ('taskId', models.ForeignKey(to_field='id', to='projects.Task', editable=False),), ('text', models.CharField(max_length=1024),), ('created', models.DateTimeField(auto_now_add=True),), ('createdBy', models.ForeignKey(to_field='id', to='projects.User', editable=False),)],
            options = {},
        ),
    ]
