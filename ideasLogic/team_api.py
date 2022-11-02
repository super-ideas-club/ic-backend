from rest_framework import serializers, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView, RetrieveAPIView, \
    DestroyAPIView, UpdateAPIView
from rest_framework.schemas.openapi import AutoSchema
from django.urls import path
from ideasLogic.models import Team, Idea
from ideasLogic.utils import check_for_banned_words


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs = {
            'created_by': {
                'read_only': True
            },
        }


class IsOwned(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.created_by.pk == request.user.pk:
            return True
        return False


class TeamSerializerToEdit(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs = {
            'created_by': {
                'read_only': True
            },
            'idea': {
                'read_only': True
            }

        }


class TeamApi(CreateAPIView):
    """
    Если мы создаем идею с самого начала (т. е. на нашли ничего похожего) <br>
    То к ней сразу создаем команду из одного человека

    Команда имеет только одну идею, я это проверяю!
    Работает
    """
    schema = AutoSchema(tags=['Team'])
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        name, description = serializer.validated_data.get('name'), serializer.validated_data.get('description')
        if not check_for_banned_words(name) or not check_for_banned_words(description):
            raise serializers.ValidationError('Do not use banned words')

        try:
            idea = serializer.validated_data.get('idea')
            team = idea.team()
            raise serializers.ValidationError('This idea already taken')
        except Team.DoesNotExist:
            pass

        return serializer.save(created_by=self.request.user)


class TeamApiEdit(DestroyAPIView, UpdateAPIView):
    """
    Эти операции может совершать только пользователеь,
    который создал команду
    """

    schema = AutoSchema(tags=['Team'])
    serializer_class = TeamSerializerToEdit
    queryset = Team.objects.all()
    permission_classes = (IsOwned, )

urlpatterns = [
    path('', TeamApi.as_view()),
    path('<int:pk>', TeamApiEdit.as_view())
]
