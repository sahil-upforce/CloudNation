import datetime
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _

from core.managers import BaseModelManager

User = get_user_model()


class BaseModel(models.Model):
    public_id = models.UUIDField(verbose_name=_("public id"), default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True)
    deleted_at = models.DateTimeField(verbose_name=_("deleted at"), null=True, blank=True)
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        verbose_name=_("updated by"),
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    deleted_by = models.ForeignKey(
        verbose_name=_("deleted by"),
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    objects = BaseModelManager()
    all_objects = BaseModelManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def hard_delete(self):
        return super().delete()


class BasePlanTypeModel(models.Model):
    FLOAT_FIELD_VALIDATOR = [MinValueValidator(0.0)]

    name = models.CharField(verbose_name=_("name"), max_length=200)
    storage = models.FloatField(verbose_name=_("storage"), help_text=_("Storage is in GB"), validators=FLOAT_FIELD_VALIDATOR)
    bandwidth = models.FloatField(verbose_name=_("bandwidth"), help_text=_("Bandwidth is in GB"), validators=FLOAT_FIELD_VALIDATOR)
    memory = models.FloatField(verbose_name=_("memory"), help_text=_("Memory is in GB"), validators=FLOAT_FIELD_VALIDATOR)
    cpu = models.FloatField(verbose_name=_("cpu"), help_text=_("CPU is in GB"), validators=FLOAT_FIELD_VALIDATOR)

    # These will change based on country
    monthly_cost = models.FloatField(verbose_name=_("monthly cost"), help_text=_("Monthly cost is in Dollar"), validators=FLOAT_FIELD_VALIDATOR)
    per_hour_cost = models.FloatField(verbose_name=_("per hour cost"), help_text=_("Per-Hour cost is in Dollar"), validators=FLOAT_FIELD_VALIDATOR)

    class Meta:
        abstract = True


class Framework(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=200)

    class Meta:
        verbose_name = "framework"
        verbose_name_plural = "frameworks"
        db_table = "frameworks"

    def __str__(self):
        return self.name


class ExternalService(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=200)

    class Meta:
        verbose_name = "External Service"
        verbose_name_plural = "External Services"
        db_table = "external_services"

    def __str__(self):
        return self.name


class ExternalServicePlanType(BaseModel, BasePlanTypeModel):
    external_service = models.ForeignKey(verbose_name=_("external service"), to=ExternalService, on_delete=models.DO_NOTHING, related_name="external_service_plan_types")

    class Meta:
        verbose_name = "External Service Plan Type"
        verbose_name_plural = "External Service Plan Types"
        db_table = "external_service_plan_types"

    def __str__(self):
        return self.name


class DatabaseType(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=200)

    class Meta:
        verbose_name = "Database Type"
        verbose_name_plural = "Database Types"
        db_table = "database_types"

    def __str__(self):
        return self.name


class DatabasePlanType(BaseModel, BasePlanTypeModel):
    database_type = models.ForeignKey(verbose_name=_("database type"), to=DatabaseType, on_delete=models.DO_NOTHING, related_name="database_plan_types")

    class Meta:
        verbose_name = "Database Plan Type"
        verbose_name_plural = "Database Plan Types"
        db_table = "database_plan_types"

    def __str__(self):
        return self.name
