from rest_framework import generics
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .custom_permissions import IsCurrentPlayerOrReadOnly, IsCurrentUserTeamMemberOrReadOnly
from players.models import Player, Team
from players.serializers import PlayerSerializer, TeamSerializer

# Create your views here.
class PlayerList(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAdminUser]

class PlayerDetail(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerManage(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # change to permission_classes = [IsCurrentPlayerOrReadOnly]
    permission_classes = [IsCurrentPlayerOrReadOnly]

class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    def get_queryset(self):
        player = self.request.user.player
        return Team.objects.filter(id__in=player.teams.values_list("id", flat=True))

class TeamCreate(generics.CreateAPIView):
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer


class TeamManage(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated & IsCurrentUserTeamMemberOrReadOnly]
    serializer_class = TeamSerializer
