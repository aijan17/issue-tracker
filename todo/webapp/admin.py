from django.contrib import admin

# Register your models here.
from webapp.models import Task, Type, Status


admin.site.register(Task)
admin.site.register(Type)
admin.site.register(Status)