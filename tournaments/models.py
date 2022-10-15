from django.conf import settings
from django.db import models
from django.utils import timezone
from players.models import Team, Player, Stats

class Game(models.Model):
    shortname = models.CharField(max_length=16)
    name = models.CharField(max_length=255)


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="tournaments")
    description = models.TextField(default=name)
    organizer = models.ForeignKey('Organizer', on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    teams = models.ManyToManyField(Team, related_name='played_tournaments', blank=True)
    hosts = models.ManyToManyField(Player, related_name='hosted_tournaments')
    max_stages = models.PositiveSmallIntegerField(default=1)
    current_stage = models.PositiveSmallIntegerField(default=1)
    is_finished = models.BooleanField(default=False)
    is_joinable = models.BooleanField(default=True)
    is_invitational = models.BooleanField(default=False)

    SINGLE_ELIMINATION = "SE"
    BRACKET_TYPE_CHOICES = [(SINGLE_ELIMINATION, "Single elimination")]
    bracket_type = models.CharField(
        max_length=2,
        choices=BRACKET_TYPE_CHOICES,
        default=SINGLE_ELIMINATION,
    )   

    def __str__(self):
        return self.name

    def stages(self):
        return range(1, self.max_stages + 1)

    def matches_of_stage(self, stage):
        return self.tournament.match_set.all().filter(stage=stage)

    def add_players(self, player_list):
        for player in player_list:
            self.players.add(player)
        self.save()



class Match(models.Model):
    team_1 = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL, related_name="matches_as_t1")
    team_2 = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL, related_name="matches_as_t2")
    start_time = models.DateTimeField(default=timezone.now)
    is_finished = models.BooleanField(default=False)
    t1_score = models.PositiveSmallIntegerField(default=0)
    t2_score = models.PositiveSmallIntegerField(default=0)
    stage = models.PositiveSmallIntegerField(default=1)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, related_name="matches")

    def winner(self):
        if self.t1_score > self.t2_score and self.is_finished:
            return self.team_1
        if self.t2_score > self.t1_score and self.is_finished:
            return self.team_2
        else:
            return None

    def __str__(self):
        return str(self.team_1) + " vs " + str(self.team_2)

class Organizer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default=name)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name