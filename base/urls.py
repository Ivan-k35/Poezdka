from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.get_directions, name='get_directions'),
    path('get_destinations/', views.get_destinations,
         name='get_destinations'),
    path('search_results/', views.search_results,
         name='search_results'),
    path('search_trip_segment/', views.search_trip_segment,
         name='search_trip_segment'),
    path('get_occupied_seats/', views.get_occupied_seats,
         name='get_occupied_seats'),
    path('start_sale_session/', views.start_sale_session,
         name='start_sale_session'),
    path('add_tickets/', views.add_tickets,
         name='add_tickets'),
]
