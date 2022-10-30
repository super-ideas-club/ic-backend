from django.contrib import admin

# Register your models here.
from ideasLogic.models import IdeaTheme, Idea


admin.site.register(Idea)
admin.site.register(IdeaTheme)