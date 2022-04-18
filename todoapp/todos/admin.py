from django.contrib import admin
from django.contrib.auth import get_user_model
from projects.models import Project
from todos.models import Todo

User = get_user_model()


class TodoAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "done", "date_created")
    list_filter = ("done", "date_created")


admin.site.register(Todo, TodoAdmin)
admin.site.register(Project)
admin.site.register(User)
