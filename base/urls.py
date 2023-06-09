from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.get_directions, name='get_directions'),
    path('get_destinations/', views.get_destinations,
         name='get_destinations'),
    path('search_trips/', views.search_trips,
         name='search_trips'),
    path('search_trip_segment/', views.search_trip_segment,
         name='search_trip_segment'),
    path('get_occupied_seats/', views.get_occupied_seats,
         name='get_occupied_seats'),
    path('start_sale_session/', views.start_sale_session,
         name='start_sale_session'),
    path('add_tickets/', views.add_tickets,
         name='add_tickets'),
    path('add_tickets_baggage/', views.add_tickets_baggage,
         name='add_tickets_baggage'),
    path('del_tickets/', views.del_tickets,
         name='del_tickets'),
    path('change_fare_name/', views.change_fare_name,
         name='change_fare_name'),
    path('set_ticket_data/', views.set_ticket_data,
         name='set_ticket_data'),
    path('reserve_order/', views.reserve_order,
         name='reserve_order'),
    path('make_payment/', views.make_payment,
         name='make_payment'),
    path('cancel_payment/', views.cancel_payment,
         name='cancel_payment'),
    path('create_return_order/', views.create_return_order,
         name='create_return_order'),
    path('add_ticket_return/', views.add_ticket_return,
         name='add_ticket_return'),
    path('delete_ticket_return/', views.delete_ticket_return,
         name='delete_ticket_return'),
    path('return_payment/', views.return_payment,
         name='return_payment'),
    path('cancel_return_payment/', views.cancel_return_payment,
         name='cancel_return_payment'),
    path('get_ticket_status/', views.get_ticket_status,
         name='get_ticket_status'),
]
