from django.urls import path
from . import views

urlpatterns = [
    path('api/nlp/tags', views.get_tags, name='get_tags'),
]