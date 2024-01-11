from django.urls import path

from hosting_management import views

urlpatterns = [
    path("deploy-app", views.ProjectAPPViewSet.as_view({"post": "create"}), name="deploy_app")
]
