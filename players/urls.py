from django.urls import path
from players.views import PlayerDetail, PlayerList, PlayerManage, TeamDetail, TeamList, TeamManage

urlpatterns = [
    path("all/", PlayerList.as_view()),
    path("<int:pk>/", PlayerDetail.as_view()),
    path("<int:pk>/teams", TeamList.as_view()),
    path("manage/<int:pk>", PlayerManage.as_view()),
    path("teams/<int:pk>", TeamDetail.as_view()),
    path("teams/manage/<int:pk>", TeamManage.as_view()),
    # path("teams/add/")

]