from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Career(models.Model):
    title = models.TextField(null=False,
                             blank=False)

    def __str__(self):
        return self.title


class Person(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_data',
                                primary_key=True)

    avatar_link = models.TextField(null=True,
                                   blank=True,
                                   default='')

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        PREFER_NOT_TO_SAY = 'N', _('Prefer not to say')

    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.PREFER_NOT_TO_SAY,
    )

    name = models.TextField(null=True,
                            blank=True,
                            default='')

    surname = models.TextField(null=True,
                               blank=True,
                               default='')

    patronymic = models.TextField(null=True,
                                  blank=True,
                                  default='')

    country = models.TextField(null=True,
                               blank=True,
                               default='')

    city = models.TextField(null=True,
                            blank=True,
                            default='')

    birth_date = models.DateField(null=True,
                                  blank=True)

    career = models.ForeignKey(Career,
                               on_delete=models.SET_NULL,
                               related_name='user_career',
                               primary_key=False,
                               null=True,
                               unique=False)

    itn = models.TextField(null=True,
                           blank=True,
                           default='')

    @classmethod
    def create(cls, user, gender,
               name, surname, country,
               city, birth_date, career,
               itn='', avatar_link='', patronymic=''):
        profile = cls(user=user, avatar_link=avatar_link,
                      gender=gender, name=name,surname=surname,
                      patronymic=patronymic, country=country,
                      city=city, birth_date=birth_date,
                      career=career, itn=itn)
        return profile

