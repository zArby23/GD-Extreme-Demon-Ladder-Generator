from django.urls import path

from ladder.views import LadderHistoryView, LadderListCreateView
from ladder.views import csrf_token, health_check


urlpatterns = [
    path("csrf/", csrf_token, name="csrf-token"),
    path("health/", health_check, name="health-check"),
    path("ladders/", LadderListCreateView.as_view(), name="ladder-list-create"),
    path("ladders/history/", LadderHistoryView.as_view(), name="ladder-history"),
]
