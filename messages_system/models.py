from django.utils import timezone

from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from users.models import Person


class Chat(models.Model):

    class ChatTypes(models.TextChoices):
        DIALOG = 'D', _('Dialog')
        CHAT = 'C', _('Chat')

    type = models.CharField(max_length=1,
                            verbose_name=_("Тип"))

    members = models.ManyToManyField(to=Person,
                                     verbose_name=_("Участники"))


class Message(models.Model):
    chat = models.ForeignKey(to=Chat,
                             on_delete=models.CASCADE,
                             verbose_name=_("Чат"))

    author = models.ForeignKey(to=Person,
                               on_delete=models.CASCADE,
                               verbose_name=_("Автор"))

    message_content = models.TextField(verbose_name=_("Сообщение"))

    pub_date = models.DateTimeField(verbose_name=_("Дата отправки"),
                                    default=timezone.now())

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message_content