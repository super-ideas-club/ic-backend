from django.template.defaulttags import url
from django.urls import path, include
from . import views

from rest_framework.schemas import get_schema_view


schema_view = get_schema_view(title="Example API")

urlpatterns = [
    path('ideas/', include("ideasLogic.ideas_api")),
    path('user-skill/', include("ideasLogic.user_skill_api")),
]