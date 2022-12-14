from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from ideasLogic.models import UserSkill
from .models import User, Person, Career

admin.site.register(UserSkill)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ['user', 'avatar_link', 'gender',
              ('name', 'surname', 'patronymic'),
              'country', 'city', 'birth_date',
              'career', 'itn']
    list_display = ['user', 'name', 'surname']


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    fields = ['title']
    list_display = ['title']
    search_fields = ['title']
