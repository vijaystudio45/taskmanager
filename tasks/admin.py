from django.contrib import admin
from .models import Team,User,Task,TaskMember

# Register your models here.
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Task)
admin.site.register(TaskMember)
