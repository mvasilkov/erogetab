from django.contrib import admin
from .models import Game, OverrideFilename

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dlsite_has_eng')

@admin.register(OverrideFilename)
class OverrideFilenameAdmin(admin.ModelAdmin):
    list_display = ('name', 'filename')
