from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


# TODO: Мб перенести в useres
from users.models import Person


class UserSkill(models.Model):
    name = models.CharField(max_length=70,
                            verbose_name="Название")

    # Одобренные теги
    approved = models.BooleanField(default=False,
                                   verbose_name="Одобрено")

    related_person = models.ManyToManyField(to=Person,
                                            blank=True,
                                            verbose_name="Люди с этими скилами")

    def __str__(self):
        return self.name


class IdeaTheme(models.Model):
    name = models.CharField(max_length=70,
                            verbose_name="Название")

    # TODO: переделать чтоб дефолтное изображение было
    background_photo = models.ImageField(blank=True,
                                         null=True,
                                         verbose_name="Изображение для фронта")

    def __str__(self):
        return self.name


class Idea(models.Model):
    short_name = models.CharField(max_length=70,
                                  verbose_name="Короткое название")

    description = models.TextField(null=True,
                                   blank=True,
                                   default='',
                                   verbose_name="Описание идеи")

    class State(models.IntegerChoices):
        CREATED = 0, _("Создано")
        TEAM_SEARCHING = 1, _("Поиск команды")
        IN_PROCESS = 2, _("Реализация")
        READY = 3, _("Готово")

    state = models.IntegerField(choices=State.choices,
                                default=State.CREATED,
                                verbose_name="Статус")

    wanted_skills = models.ManyToManyField(to=UserSkill,
                                           verbose_name="Требуемые скиллы")

    main_theme = models.ForeignKey(to=IdeaTheme,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   verbose_name="Тема")

    # team = models.ForeignKey()

    def __str__(self):
        return self.short_name