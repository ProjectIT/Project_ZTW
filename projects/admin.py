from django.contrib import admin

from projects.models import UserProfile, Friends, Project, Task, TaskComment, File, PersonInProject

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(File)
admin.site.register(PersonInProject)
admin.site.register(Friends)