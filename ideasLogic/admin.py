from django.contrib import admin

# Register your models here.
from ideasLogic.models import IdeaTheme, Idea, Team

admin.site.register(Idea)
admin.site.register(IdeaTheme)
admin.site.register(Team)