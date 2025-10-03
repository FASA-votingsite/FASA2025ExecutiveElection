from django.urls import path
from . import views

urlpatterns = [
    path('', views.election_list, name='election_list'),
    path('positions/', views.position_list, name='position_list'),
    path('candidates/', views.candidate_list, name='candidate_list'),
]