from django.contrib import admin

# Register your models here.
from messages_system.models import Message, Chat

admin.site.register(Message)
admin.site.register(Chat)