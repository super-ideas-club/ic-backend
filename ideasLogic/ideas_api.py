from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, GenericAPIView, RetrieveAPIView, \
    DestroyAPIView, UpdateAPIView
from rest_framework.schemas.openapi import AutoSchema

from ideasLogic.models import IdeaTheme, Idea
from django.urls import path

from ideasLogic.utils import check_for_banned_words


class IdeaThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaTheme
        fields = ('pk', 'name', 'background_photo',)


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ('pk', 'short_name', 'description', 'state', 'main_theme', 'wanted_skills', )
        extra_kwargs = {
            'state': {
                'read_only': True
            },
            'pk': {
                'read_only': True
            }
        }


class IdeaThemeList(ListAPIView):
    """
    Работает
    """
    schema = AutoSchema(tags=["Idea"])
    serializer_class = IdeaThemeSerializer

    def get_queryset(self):
        return IdeaTheme.objects.all()


class IdeaThemeCreate(CreateAPIView):
    """
    Работает
    """
    schema = AutoSchema(tags=["Idea"])
    serializer_class = IdeaThemeSerializer

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        if not check_for_banned_words(name):
            raise serializers.ValidationError('Do not use banned words')
        return serializer.save()


class IdeaCreate(CreateAPIView):
    """
    Работает
    """
    schema = AutoSchema(tags=["Idea"])
    serializer_class = IdeaSerializer
    queryset = Idea.objects.all()

    def perform_create(self, serializer):
        short_name = serializer.validated_data.get('short_name')
        description = serializer.validated_data.get('description')
        if not check_for_banned_words(short_name) or not check_for_banned_words(description):
            raise serializers.ValidationError('Do not use banned words')
        return serializer.save()


class IdeaGetDelete(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    """
    Работает
    """
    schema = AutoSchema(tags=["Idea"])
    serializer_class = IdeaSerializer
    queryset = Idea.objects.all()


urlpatterns = [
    path('themes/all', IdeaThemeList.as_view(), name='idea_theme_all'),
    path('themes/create', IdeaThemeCreate.as_view(), name='create_idea_theme'),
    path('create', IdeaCreate.as_view()),
    path('<int:pk>', IdeaGetDelete.as_view())
]