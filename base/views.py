import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from zeep import Client
from zeep.helpers import serialize_object
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from dotenv import load_dotenv

load_dotenv()


def get_directions(request):
    url = "http://dev.avibus.pro/UEEDev/ws/SchedulePort?wsdl"
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    session = Session()
    session.auth = HTTPBasicAuth(username, password)
    client = Client(wsdl=url, transport=Transport(session=session))

    bus_stops = client.service.GetBusStops()

    travel_directions = [{'id': td.Id, 'name': td.Name} for td in bus_stops if td.Automated]
    return render(request, 'base/home_page.html', {'travel_directions': travel_directions})


def get_destinations(request):
    url = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    session = Session()
    session.auth = HTTPBasicAuth(username, password)
    client = Client(wsdl=url, transport=Transport(session=session))

    service = client.service
    available_methods = service.__dir__()

    # Вывод списка доступных методов
    for method_name in available_methods:
        print(method_name)

    departure_id = request.POST.get('travel_direction')
    departure_name = request.POST.get('travel_direction_name')
    destinations = client.service.GetDestinations(Departure=departure_id, Substring='')

    if destinations:
        end_directions = [{'id': dis.Id, 'name': dis.Name} for dis in destinations]
    else:
        end_directions = None
    context = {'end_directions': end_directions, 'departure': departure_id,
               'departure_name': departure_name}
    return render(request, 'base/search_bus.html', context=context)


def search_results(request):
    # Получение параметров запроса из GET-параметров
    departure = request.POST.get('start_direction')
    destination = request.POST.get('end_direction')
    date = '2023-06-01'

    # Логика вызова API и обработки результатов поиска
    url = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
    username = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    session = Session()
    session.auth = HTTPBasicAuth(username, password)
    client = Client(wsdl=url, transport=Transport(session=session))

    bus_results = client.service.GetTrips(Departure=departure, Destination=destination, TripsDate=date)
    bus_results_ser = serialize_object(bus_results)

    # context = {'departure': departure, 'destination': destination, 'date': date, 'bus_results': bus_results_ser}
    # print(type(bus_results))
    # return render(request, 'base/search_results.html', context=context)
    return JsonResponse(bus_results_ser)


