from django.contrib.auth.models import User
from django.db.models import When
from rest_framework import serializers
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
        fields = ('pk', 'short_name', 'description', 'state', 'themes', 'wanted_skills', 'hidden')
        depth = 1
        extra_kwargs = {
            'state': {
                'read_only': True
            },
            'pk': {
                'read_only': True
            }
        }


class IdeaSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ('pk', 'short_name', 'description', 'state', 'themes', 'hidden')
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
    serializer_class = IdeaSerializerCreate
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


class IdeasList(ListAPIView):
    """
    Работает!
    Выдает список откртых идей по конкретному пользователю

    Если пользотель запрашивает свои идеи (или это администратор) то выдает в том числе скрытые идеи
    """

    serializer_class = IdeaSerializer
    schema = AutoSchema(tags=["Team"], operation_id_base="ideas list by user")

    def get_queryset(self):
        from ideasLogic.models import Team
        needed_user = self.kwargs['user_id']
        users_teams = Team.objects.filter(persons__user=needed_user)
        print(users_teams)
        query_set = Idea.objects.filter(team__in=users_teams)

        all_users_in_teams = users_teams.values_list('persons')
        print(all_users_in_teams)

        try:
            user = self.request.user
            res = When(user__in=all_users_in_teams, then=True)
            if not (user.is_staff or res):
                query_set = query_set.filter(hidden=False)
        except User.DoesNotExist:
            pass
            query_set = query_set.filter(hidden=False)

        return query_set


class IdeasByThemes(ListAPIView):
    serializer_class = IdeaSerializer

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        themes_ids = []
        print(self.request.data)
        if self.request.data['themes_ids']:
            themes_ids = self.request.data['themes_ids']
        print(themes_ids)
        if len(themes_ids) == 0:
            return Idea.objects.filter(hidden=False)

        return Idea.objects.filter(themes__in=themes_ids, hidden=False).distinct()



urlpatterns = [
    path('themes/all', IdeaThemeList.as_view(), name='idea_theme_all'),
    path('themes/create', IdeaThemeCreate.as_view(), name='create_idea_theme'),
    path('create', IdeaCreate.as_view()),
    path('list/<int:user_id>', IdeasList.as_view()),
    path('<int:pk>', IdeaGetDelete.as_view()),
    path('by-themes', IdeasByThemes.as_view()),
]

