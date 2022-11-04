from django.db.models import When
from django.urls import path
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.schemas.openapi import AutoSchema

from messages_system.models import Message, Chat
from users.models import Person


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        depth = 1


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        depth = 1


class MessageCreateSerializer(serializers.Serializer):
    message_content = serializers.CharField()
    to_users = serializers.ListField(child=serializers.IntegerField())
    schema = AutoSchema(tags=["Messages"])

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class MessagesByChat(ListAPIView):
    serializer_class = MessagesSerializer
    """
    Работает  <br>
    
    Выдача сообщений по определенному чату  <br>
    Доступно, если ты участник чата
    """

    schema = AutoSchema(tags=["Messages"])

    def get_queryset(self):
        chat = Chat.objects.get(pk=self.kwargs['chat_id'])
        user = self.request.user
        res = When(user__in=chat.members.values_list('user'), then=True)
        if res:
            return Message.objects.filter(chat=self.kwargs['chat_id'])
        return []


class ChatsList(ListAPIView):
    serializer_class = ChatSerializer
    """
    Работает <br>
    Чаты пользователя <br>
    
    Пользотваель может увидеть только свои чаты
    """
    schema = AutoSchema(tags=["Messages"])

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(members__user=user)


class SendMessage(CreateAPIView):
    """
    Работает <br>

    Отправить сообщение <br>
    Если чат пустой - создадим новый
    """
    serializer_class = MessageCreateSerializer
    schema = AutoSchema(tags=["Messages"], )

    def perform_create(self, serializer):
        from_user = self.request.user
        users_id = serializer.validated_data.get('to_users')
        users = []
        for user in users_id:
            try:
                user_obj = Person.objects.get(pk=user)
                users.append(user_obj)
            except Person.DoesNotExist:
                users_id.remove(user)
                raise serializers.ValidationError('User with this id dosesnt exists: ', user)

        author = Person.objects.get(user=from_user)
        users.append(author)

        try:
            chat_objects = Chat.objects.filter(members__in=users_id)
            need_create_new_chat = True
            for item in chat_objects:
                if len(item.members.all()) == len(users):
                    need_create_new_chat = False
                    chat = item

        except Chat.DoesNotExist:
            need_create_new_chat = True

        if need_create_new_chat:
            chat_type = 'D'
            print(len(users))
            if len(users) > 2:
                chat_type = 'C'
            chat = Chat(type=chat_type)
            chat.save()
            for user in users:
                chat.members.add(user)
            chat.save()

        new_message = Message(message_content=serializer.validated_data.get('message_content'),
                              chat=chat,
                              author=author)

        return new_message.save()


urlpatterns = [
    path('by-chat/<int:chat_id>', MessagesByChat.as_view()),
    path('chat-list', ChatsList.as_view()),
    path('send', SendMessage.as_view())
]
