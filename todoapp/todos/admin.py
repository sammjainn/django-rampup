from django.contrib import admin

from todos.models import Todo
from projects.models import Project


class TodoAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "done", "date_created")
    list_filter = ("done", "date_created")


admin.site.register(Todo, TodoAdmin)
admin.site.register(Project)
