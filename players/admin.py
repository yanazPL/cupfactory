from django.contrib import admin
from .models import Player, Stats, Team

class TeamAdmin(admin.ModelAdmin):
    exclude = ("stats",)

admin.site.register(Player)
admin.site.register(Stats)
admin.site.register(Team, TeamAdmin)