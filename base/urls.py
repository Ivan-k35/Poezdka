from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.get_directions, name='get_directions'),
    path('get_destinations/', views.get_destinations,
         name='get_destinations'),
    path('search_results/', views.search_results,
         name='search_results'),
]
