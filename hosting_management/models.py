from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, DatabasePlanType, ExternalServicePlanType, Framework

User = get_user_model()


class Project(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=200)
    # have Multiple Owners
    owner = models.ForeignKey(verbose_name=_("owner"), to=User, on_delete=models.DO_NOTHING, related_name="projects")

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        db_table = "projects"

    def __str__(self):
        return self.name


class ProjectAPP(BaseModel):
    STATUS_CHOICES = (
        ("CR", "Created"),
        ("PD", "Pending"),
        ("IP", "In Progress"),
        ("DP", "Deployed"),
        ("TM", "Terminated"),
        ("ST", "Stopped"),
        ("FL", "Failed"),
    )

    name = models.CharField(verbose_name=_("name"), max_length=200)
    project = models.ForeignKey(verbose_name=_("project"), to=Project, on_delete=models.DO_NOTHING, related_name="apps")
    framework = models.ForeignKey(
        verbose_name=_("framework"),
        to=Framework,
        on_delete=models.DO_NOTHING,
        related_name="apps",
    )
    external_service_plan_type = models.ForeignKey(
        verbose_name=_("external service plan type"),
        to=ExternalServicePlanType,
        on_delete=models.DO_NOTHING,
        related_name="apps"
    )
    database_plan_type = models.ForeignKey(
        verbose_name=_("database plan type"),
        to=DatabasePlanType,
        on_delete=models.DO_NOTHING,
        related_name="apps",
        null=True,
        blank=True
    )
    status = models.CharField(verbose_name=_("status"), max_length=10, choices=STATUS_CHOICES, default="CR")

    # Region will add based on country
    # region = models.ForeignKey(verbose_name=_("region"), to=Region, on_delete=models.DO_NOTHING, related_name="apps")

    class Meta:
        verbose_name = "APP"
        verbose_name_plural = "APPs"
        db_table = "apps"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'project'], condition=Q(deleted_at__isnull=True), name='name_project_unique_constraint'
        )]

    def __str__(self):
        return self.name


class EnvironmentVariable(BaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=200)
    value = models.CharField(verbose_name=_("value"), max_length=1000)
    app = models.ForeignKey(
        verbose_name=_("app"),
        to=ProjectAPP,
        on_delete=models.CASCADE,
        related_name="environment_variables"
    )

    # Can add type - Ex: Str, Int, Float ...

    class Meta:
        verbose_name = "Environment Variable"
        verbose_name_plural = "Environment Variables"
        db_table = "environment_variables"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'app'], condition=Q(deleted_at__isnull=True), name='name_app_unique_constraint'
            )]

    def __str__(self):
        return self.name
