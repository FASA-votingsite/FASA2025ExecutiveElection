from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote_list, name='vote_list'),
    path('cast/', views.cast_vote, name='cast_vote'),
    path('results/', views.election_results, name='election_results'),
]