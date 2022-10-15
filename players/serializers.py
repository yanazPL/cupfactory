from django.forms import CharField
from rest_framework import serializers
from .models import Player, Team

class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username", read_only=True)
    class Meta:

        model = Player
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):
    players = serializers.PrimaryKeyRelatedField(many=True, queryset=Player.objects.all())
    player_names = serializers.SerializerMethodField('get_player_names')

    def get_player_names(self, team):
        return [str(player) for player in team.players.all()]

    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ("stats",)