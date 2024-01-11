from uuid import UUID

from django.db import transaction
from rest_framework import serializers

from core.serializers import BaseSerializer
from hosting_management.models import (
    DatabasePlanType, EnvironmentVariable, ExternalServicePlanType, Framework, Project, ProjectAPP
)


class EnvironmentVariableSerializer(BaseSerializer):
    name = serializers.CharField(required=True, max_length=200, allow_blank=False)
    value = serializers.CharField(required=True, max_length=1000, allow_blank=False)

    class Meta:
        model = EnvironmentVariable
        fields = (*BaseSerializer.Meta.fields, "name", "value")
        read_only_fields = (*BaseSerializer.Meta.fields,)
        extra_kwargs = {"name": {"required": True}, "value": {"required": True}}


class CreateProjectAPPSerializer(BaseSerializer, serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    framework_id = serializers.PrimaryKeyRelatedField(queryset=Framework.objects.all(), required=True)
    external_service_plan_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ExternalServicePlanType.objects.all(), required=True
    )
    database_plan_type_id = serializers.PrimaryKeyRelatedField(queryset=DatabasePlanType.objects.all(), required=False)
    environment_variables = EnvironmentVariableSerializer(many=True, required=False)

    class Meta:
        model = ProjectAPP
        fields = (
            *BaseSerializer.Meta.fields,
            "name",
            "status",
            "project_id",
            "framework_id",
            "external_service_plan_type_id",
            "database_plan_type_id",
            "environment_variables"
        )
        read_only_fields = (*BaseSerializer.Meta.fields, "status")

    def validate_name(self, value):
        project_id = self.initial_data["project_id"]
        if ProjectAPP.objects.filter(name=value, project_id=project_id).exists():
            raise serializers.ValidationError(f"App name is already exists with project id {project_id}")
        return value

    def validate_project_id(self, value):
        return value.pk

    def validate_framework_id(self, value):
        return value.pk

    def validate_external_service_plan_type_id(self, value):
        return value.pk

    def validate_database_plan_type_id(self, value):
        return value.pk

    def validate_environment_variables(self, value):
        names = [item['name'] for item in value]
        if len(names) != len(set(names)):
            raise serializers.ValidationError("Environment variable names must be unique.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            environment_variables_data = validated_data.pop("environment_variables", [])
            app = ProjectAPP.objects.create(**validated_data)
            environment_variable_serializer = EnvironmentVariableSerializer(data=environment_variables_data, many=True)
            environment_variable_serializer.is_valid(raise_exception=True)
            environment_variables = [
                EnvironmentVariable(app=app, **env_var_data)
                for env_var_data in environment_variable_serializer.validated_data
            ]
            EnvironmentVariable.objects.bulk_create(environment_variables)
        return app
