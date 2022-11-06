from django.contrib import admin

# Register your models here.
from ideasLogic.models import IdeaTheme, Idea, Team

admin.site.register(Idea)
admin.site.register(IdeaTheme)
admin.site.register(Team)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    fields = ['short_name', 'description', 'state', 'wanted_skills', 'themes', 'hidden']
    list_filter = ['themes']

