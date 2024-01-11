from django.contrib import admin

from core.models import (
    BaseModel, DatabaseType, DatabasePlanType, ExternalService, ExternalServicePlanType, Framework
)


class BaseAdmin(admin.ModelAdmin):
    exclude = tuple(field.name for field in BaseModel._meta.fields)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DatabaseType)
class DatabaseTypeAdmin(BaseAdmin):
    pass


@admin.register(DatabasePlanType)
class DatabasePlanTypeAdmin(BaseAdmin):
    pass


@admin.register(ExternalService)
class ExternalServiceAdmin(BaseAdmin):
    pass


@admin.register(ExternalServicePlanType)
class ExternalServicePlanTypeAdmin(BaseAdmin):
    pass


@admin.register(Framework)
class FrameworkAdmin(BaseAdmin):
    pass

