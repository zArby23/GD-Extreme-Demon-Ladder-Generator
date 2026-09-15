from django.urls import path

from ladder.views import LadderHistoryView, LadderListCreateView


urlpatterns = [
    path("ladders/", LadderListCreateView.as_view(), name="ladder-list-create"),
    path("ladders/history/", LadderHistoryView.as_view(), name="ladder-history"),
]
