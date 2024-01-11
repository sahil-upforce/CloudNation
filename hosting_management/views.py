from rest_framework import viewsets

from hosting_management.models import ProjectAPP
from hosting_management.serializers import CreateProjectAPPSerializer


class ProjectAPPViewSet(viewsets.ModelViewSet):
    queryset = ProjectAPP.objects.all()
    serializer_class = CreateProjectAPPSerializer
