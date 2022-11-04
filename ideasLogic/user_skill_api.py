import json

from django.http import JsonResponse
from django.urls import path
from rest_framework import serializers, status, filters
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, GenericAPIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from ideasLogic.models import UserSkill
from ideasLogic.utils import check_for_banned_words
from users.models import Person


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'
        extra_kwargs = {
            'approved': {
                'read_only': True
            }
        }


class AddSkillRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    skills_id = serializers.ListField(child=serializers.IntegerField())

    def update(self, instance, validated_data):
        pass

    def create(self, attrs):
        user_id = attrs.get('user_id')
        try:
            user = Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            raise serializers.ValidationError('User with this id dosesnt exists: ', user_id)
        skills = []

        for skill_id in attrs.get('skills_id'):
            try:
                skill = UserSkill.objects.get(pk=skill_id)
            except UserSkill.DoesNotExist:
                raise serializers.ValidationError(f"UserSkill with pk {skill_id} doesn't exist")
            else:
                skills.append(skill)

        return [user, skills]


class UserSkillList(ListAPIView):
    """
    Работает
    Выдает только запрувленные скиллы
    """
    schema = AutoSchema(tags=["UserSkill"])
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return UserSkill.objects.filter(approved=True)


class UserSkillListByUser(ListAPIView):
    """
    Работает
    Выдает только скилы, которые относятся к пользователю
    """
    schema = AutoSchema(tags=["UserSkill"], operation_id_base="by user")
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return UserSkill.objects.filter(related_person__pk=self.kwargs['pk'])


class UserSkillMain(CreateAPIView):
    """
    Работает
    """
    schema = AutoSchema(tags=["UserSkill"])
    serializer_class = UserSkillSerializer
    queryset = Person.objects.all()

    def perform_create(self, serializer):

        name = serializer.data.get('name')
        if not check_for_banned_words(name):
            raise serializers.ValidationError('Do not use banned words')

        skill = UserSkill(name=name)
        skill.save()
        skill.related_person.add(
            Person.objects.get(pk=serializer.data.get('related_person')[0]))
        skill.save()
        return JsonResponse(status=status.HTTP_201_CREATED,
                            data={
                                'message': 'Idea Saved',
                            })


class AddSkillsToUser(GenericAPIView):
    """
    Работает
    Установить набор скиллов пользотелю
    Он перезаписывает значения!! Т. е сначала нужно получить весь список скиллов
    """
    schema = AutoSchema(tags=["UserSkill"])
    serializer_class = AddSkillRequestSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def put(self, request):
        serializer = self.get_serializer()
        user, skills = serializer.create(request.data)
        old_skills = UserSkill.objects.filter(related_person=user)
        for skill in old_skills:
            if not skill in skills:
                skill.related_person.remove(user)
                skill.save()

        for skill in skills:
            if not skill in old_skills:
                skill.related_person.add(user)
                skill.save()

        return JsonResponse(status=status.HTTP_200_OK,
                            data={
                                'message': 'Skills set',
                            })


urlpatterns = [
    path('all', UserSkillList.as_view(), name='all_user_skills'),
    path('create', UserSkillMain.as_view(), name='create_user_skill'),
    path('by-user/<int:pk>', UserSkillListByUser.as_view()),
    path('by-user/set', AddSkillsToUser.as_view()),
]
