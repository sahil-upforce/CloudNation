from django.contrib import admin

from core.admin import BaseAdmin
from hosting_management.models import EnvironmentVariable, Project, ProjectAPP


@admin.register(EnvironmentVariable)
class EnvironmentVariableAdmin(BaseAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    pass


@admin.register(ProjectAPP)
class ProjectAPPAdmin(BaseAdmin):
    pass
