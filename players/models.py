from re import L
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @receiver(post_save, sender=get_user_model())
    def create_player_profile(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

    def __str__(self):
        return self.user.username



class Team(models.Model):
    name = models.CharField(max_length=150)
    players = models.ManyToManyField('Player', related_name="teams")
    stats = models.OneToOneField("Stats", on_delete=models.CASCADE, null=True)

    def __str__(self):
        if len(self.players.all()) == 1:
            return str(self.players.first())
        else:
            return self.name

class Stats(models.Model):
    wins = models.PositiveIntegerField(default=0)
    loses = models.PositiveIntegerField(default=0)
    @receiver(post_save, sender=Team)
    def create_team_stats(sender, instance, created, **kwargs):
        if created:
            Stats.objects.create(team=instance)
  
  

        
        