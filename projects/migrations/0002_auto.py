# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('projects', '0001_initial')]

    operations = [
        migrations.AlterField(
            name = 'projectId',
            field = models.ForeignKey(editable=False, to_field='id', to='projects.Project', null=True),
            model_name = 'file',
        ),
        migrations.AlterField(
            name = 'path',
            field = models.FileField(upload_to='projects/attachments'),
            model_name = 'file',
        ),
        migrations.AlterField(
            name = 'taskId',
            field = models.ForeignKey(editable=False, to_field='id', to='projects.Task', null=True),
            model_name = 'file',
        ),
        migrations.RemoveField(
            name = 'status',
            model_name = 'task',
        ),
        migrations.AlterField(
            name = 'projectId',
            field = models.ForeignKey(null=True, blank=True, default=None, to='projects.Project', to_field='id'),
            model_name = 'task',
        ),
        migrations.AlterField(
            name = 'type',
            field = models.CharField(choices=(('B', 'Bug',), ('I', 'Improvement',), ('F', 'New Feature',), ('O', 'Other',),), max_length=1, default='T'),
            model_name = 'task',
        ),
        migrations.AlterField(
            name = 'personResponsible',
            field = models.ForeignKey(null=True, blank=True, default=None, to='projects.User', to_field='id'),
            model_name = 'task',
        ),
        migrations.AlterField(
            name = 'description',
            field = models.CharField(max_length=1024, blank=True),
            model_name = 'project',
        ),
        migrations.AddField(
            name = 'avatarPath',
            field = models.CharField(editable=False, max_length=128, default='stub_imgs/avatar2.jpg'),
            model_name = 'user',
        ),
    ]
