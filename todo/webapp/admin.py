from django.contrib import admin

from webapp.models import Task, Type, Status, Project,Projects_tasks

admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Projects_tasks)
