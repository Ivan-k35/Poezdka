import os
from django.http import JsonResponse
from django.shortcuts import render
from zeep import Client
from zeep.helpers import serialize_object
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from dotenv import load_dotenv

load_dotenv()

WSDL_SCHEDULE = "http://dev.avibus.pro/UEEDev/ws/SchedulePort?wsdl"
WSDL_SALE = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
USERNAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')


def get_client(wsdl):
    session = Session()
    session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
    client = Client(wsdl=wsdl, transport=Transport(session=session))
    return client


def get_directions(request):
    client = get_client(WSDL_SCHEDULE)
    bus_stops = client.service.GetBusStops()
    travel_directions = [{'id': td.Id, 'name': td.Name} for td in bus_stops if td.Automated]
    return JsonResponse({'travel_directions': travel_directions})


def get_destinations(request):
    client = get_client(WSDL_SALE)
    departure_id = '862fd93e-e633-11e7-80e7-00175d776a07'  # request.POST.get('travel_direction')
    destinations = client.service.GetDestinations(Departure=departure_id, Substring='')

    end_directions = [{'id': dis.Id, 'name': dis.Name} for dis in destinations] if destinations else None

    return JsonResponse({'end_directions': end_directions, 'departure': departure_id})


def search_trips(request):
    departure = '862fd93e-e633-11e7-80e7-00175d776a07'  # request.POST.get('start_direction')
    destination = 'cb654d84-f487-11ed-83c7-d00da3a6c886'  # request.POST.get('end_direction')
    date = '2023-06-08'

    client = get_client(WSDL_SALE)
    bus_results = client.service.GetTrips(Departure=departure, Destination=destination, TripsDate=date)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def search_trip_segment(request):
    departure = 'cb654d84-f487-11ed-83c7-d00da3a6c886'
    destination = '862fd93e-e633-11e7-80e7-00175d776a07'
    trip_id = '38871dbb-dffe-11e7-80e7-00175d776a078ef8b472-fcd3-11ed-0591-d00d5ddf9041'

    client = get_client(WSDL_SALE)
    bus_results = client.service.GetTripSegment(TripId=trip_id, Departure=departure, Destination=destination)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def get_occupied_seats(request):
    departure = 'cb654d84-f487-11ed-83c7-d00da3a6c886'
    destination = '862fd93e-e633-11e7-80e7-00175d776a07'
    trip_id = '38871dbb-dffe-11e7-80e7-00175d776a07b9e9dbb0-fd9c-11ed-399e-d00d5ddf9041'
    order_id = ''

    client = get_client(WSDL_SALE)
    bus_results = client.service.GetOccupiedSeats(TripId=trip_id, Departure=departure,
                                                  Destination=destination, OrderId=order_id)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def start_sale_session(request):
    departure = 'cb654d84-f487-11ed-83c7-d00da3a6c886'
    destination = '862fd93e-e633-11e7-80e7-00175d776a07'
    trip_id = '38871dbb-dffe-11e7-80e7-00175d776a078ef8b472-fcd3-11ed-0591-d00d5ddf9041'
    order_id = ''

    client = get_client(WSDL_SALE)
    bus_results = client.service.StartSaleSession(TripId=trip_id, Departure=departure,
                                                  Destination=destination, OrderId=order_id)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def add_tickets(request):
    order_id = '00000026685'

    ticket_seats = {
        'Elements': {
            'FareName': 'Пассажирский',
            'SeatNum': '0',
            'ParentTicketSeatNum': '0'
        }
    }

    client = get_client(WSDL_SALE)
    bus_results = client.service.AddTickets(OrderId=order_id, TicketSeats=ticket_seats)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def add_tickets_baggage(request):
    order_id = '00000026685'

    ticket_seats = {
        'Elements': {
            'FareName': 'Багажный',
            'SeatNum': '0',
            'ParentTicketSeatNum': '1'
        }
    }

    client = get_client(WSDL_SALE)
    bus_results = client.service.AddTickets(OrderId=order_id, TicketSeats=ticket_seats)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def del_tickets(request):
    order_id = '00000026685'

    ticket_seats = {
        'Elements': {
            'FareName': 'Пассажирский',
            'SeatNum': '3'
        }
    }

    client = get_client(WSDL_SALE)
    bus_results = client.service.DelTickets(OrderId=order_id, TicketSeats=ticket_seats)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def change_fare_name(request):
    """
    Смена тарифа
    """
    order_id = '00000026685'

    tickets = {
        'Elements': {
            'Number': '01000000072020',
            'SeatNum': '2',
            'FareName': 'Детский'

        }
    }

    client = get_client(WSDL_SALE)
    bus_results = client.service.SetTicketData(OrderId=order_id, Tickets=tickets)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


# def set_ticket_date(request):
#     """
#     Заполнение данных по билетам
#     """
#     order_id = '00000026685'
#
#     tickets = {
#         'Elements': {
#             'Number': '01000000072020',
#             'SeatNum': '10',
#             'FareName': 'Пассажирский',
#             'PersonalData': {
#                 'Name': 'ФИО',
#                 'Value': 'Дроздов Щегол Филинович'
#             },
#             'PersonalData': {
#                 'Name': 'Удостоверение',
#                 'Value': 'II-АБ 123456',
#                 'ValueKind': 'Свидетельство о рождении'
#             },
#             'PersonalData': {
#                 'Name': 'Дата рождения',
#                 'Value': '2010-02-25T00:00:00'
#             },
#             'PersonalData': {
#                 'Name': 'Пол',
#                 'Value': 'Мужской'
#             },
#             'PersonalData': {
#                 'Name': 'Гражданство',
#                 'Value': 'РОССИЯ'
#             }
#         },
#         'Elements': {
#             'Number': '01000000072051',
#             'ParentTicketSeatNum': '10',
#             'SeatNum': '2',
#             'FareName': 'Багажный'
#         },
#         'Elements': {
#             'Number': '01000000072013',
#             'SeatNum': '11',
#             'FareName': 'Детский',
#             'PersonalData': {
#                 'Name': 'ФИО',
#                 'Value': 'Дроздов Перепел Щеглович</'
#             },
#             'PersonalData': {
#                 'Name': 'Удостоверение',
#                 'Value': 'II-АБ 123456',
#                 'ValueKind': 'Свидетельство о рождении'
#             },
#             'PersonalData': {
#                 'Name': 'Дата рождения',
#                 'Value': '2010-02-25T00:00:00'
#             },
#             'PersonalData': {
#                 'Name': 'Пол',
#                 'Value': 'Мужской'
#             },
#             'PersonalData': {
#                 'Name': 'Гражданство',
#                 'Value': 'РОССИЯ'
#             }
#         },
#         'Elements': {
#             'Number': '01000000072051',
#             'ParentTicketSeatNum': '10',
#             'SeatNum': '2',
#             'FareName': 'Багажный'
#         },
#
#     }
#
#     client = get_client(WSDL_SALE)
#     bus_results = client.service.SetTicketData(OrderId=order_id, Tickets=tickets)
#     bus_results_ser = serialize_object(bus_results)
#
#     return JsonResponse(bus_results_ser)

def set_ticket_data(request):
    """
    Установка данных билета
    """
    order_id = '00000022788'

    tickets = {
        'Elements': [
            {
                'Number': '01000000072044',
                'SeatNum': '10',
                'FareName': 'Пассажирский',
                'PersonalData': [
                    {'Name': 'ФИО', 'Value': 'Дроздов Щегол Филинович'},
                    {'Name': 'Удостоверение', 'Value': '98 76 543210', 'ValueKind': 'Паспорт гражданина РФ'},
                    {'Name': 'Дата рождения', 'Value': '1980-02-25T00:00:00'},
                    {'Name': 'Пол', 'Value': 'Мужской'},
                    {'Name': 'Гражданство', 'Value': 'РОССИЯ'},
                ]
            },
            {
                'Number': '01000000072051',
                'ParentTicketSeatNum': '10',
                'SeatNum': '2',
                'FareName': 'Багажный'
            },
            {
                'Number': '01000000072013',
                'SeatNum': '11',
                'FareName': 'Детский',
                'PersonalData': [
                    {'Name': 'ФИО', 'Value': 'Дроздов Перепел Щеглович'},
                    {'Name': 'Удостоверение', 'Value': 'II-АБ 123456', 'ValueKind': 'Свидетельство о рождении'},
                    {'Name': 'Дата рождения', 'Value': '2010-02-25T00:00:00'},
                    {'Name': 'Пол', 'Value': 'Мужской'},
                    {'Name': 'Гражданство', 'Value': 'РОССИЯ'},
                ]
            },
            {
                'Number': '01000000072051',
                'ParentTicketSeatNum': '10',
                'SeatNum': '2',
                'FareName': 'Багажный'
            },
        ]
    }

    client = get_client(WSDL_SALE)
    bus_results = client.service.SetTicketData(OrderId=order_id, Tickets=tickets)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def reserve_order(request):
    """
    Бронирование заказа для оплаты
    """
    order_id = '00000022788'
    customer = {'Email': 'example@mail.com'}
    reserve_kind = ''
    cheque_settings = {'ChequeWidth': '48'}
    client = get_client(WSDL_SALE)
    bus_results = client.service.ReserveOrder(OrderId=order_id, Customer=customer,
                                              ReserveKind=reserve_kind, ChequeSettings=cheque_settings)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def make_payment(request):
    """
    Оплата заказа
    """
    order_id = '00000022788'
    terminal_id = ''
    terminal_session_id = ''
    payment_items = {
        'Elements': {
            'PaymentType': 'PaymentCard',
            'Amount': 'Amount'
        }
    }
    cheque_settings = {'ChequeWidth': '48'}
    client = get_client(WSDL_SALE)
    bus_results = client.service.Payment(OrderId=order_id, TerminalId=terminal_id,
                                         TerminalSessionId=terminal_session_id,
                                         PaymentItems=payment_items,
                                         ChequeSettings=cheque_settings)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def create_return_order(request):
    """
    Создает заказ на возврат билета в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом создания заказа на возврат.
    """
    ticket_number = '0100000000701'
    seat_num = '0'
    departure = 'ba40c9a8-a30f-11e5-9c4b-74d4354448bc'
    return_order_id = ''

    client = get_client(WSDL_SALE)
    bus_results = client.service.AddTicketReturn(
        TicketNumber=ticket_number,
        SeatNum=seat_num,
        Departure=departure,
        ReturnOrderId=return_order_id
    )
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def add_ticket_return(request):
    """
    Добавляет билет для возврата в заказ для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом добавления билета для возврата в заказ.
    """
    return_order_id = '00000010663'
    ticket_number = '01000000072013'
    seat_num = '0'
    departure = 'ba40c9a8-a30f-11e5-9c4b-74d4354448bc'

    client = get_client(WSDL_SALE)
    bus_results = client.service.AddTicketReturn(TicketNumber=ticket_number,
                                                 SeatNum=seat_num,
                                                 Departure=departure,
                                                 ReturnOrderId=return_order_id)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def delete_ticket_return(request):
    """
    Удаляет билет из возврата в заказе для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом удаления билета из возврата в заказе.
    """
    return_order_id = '00000010663'
    ticket_number = '01000000072013'

    client = get_client(WSDL_SALE)
    bus_results = client.service.DelTicketReturn(ReturnOrderId=return_order_id,
                                                 TicketNumber=ticket_number)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def return_payment(request):
    """
    Возвращает заказ в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом возврата заказа.
    """
    return_order_id = '00000010663'
    terminal_id = ''
    terminal_session_id = ''

    payment_items = """
        <PaymentItems xmlns="http://www.unistation.ru/xdto" xmlns:xs="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="PaymentItems"/>
    """

    cheque_settings = """
        <ChequeSettings xmlns="http://www.unistation.ru/xdto" xmlns:xs="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ChequeSettings">
            <ChequeWidth>48</ChequeWidth>
        </ChequeSettings>
    """

    client = get_client(WSDL_SALE)
    bus_results = client.service.ReturnPayment(ReturnOrderId=return_order_id,
                                               TerminalId=terminal_id,
                                               TerminalSessionId=terminal_session_id,
                                               PaymentItems=payment_items,
                                               ChequeSettings=cheque_settings)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def cancel_return_payment(request):
    """
    Отменяет возврат заказа в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом отмены возврата заказа.
    """
    return_order_id = '00000010663'
    ticket_seats = ''
    services = ''
    payment_items = ''
    client = get_client(WSDL_SALE)
    bus_results = client.service.CancelReturnPayment(ReturnOrderId=return_order_id, TicketSeats=ticket_seats,
                                                     Services=services, PaymentItems=payment_items)
    bus_results_ser = serialize_object(bus_results)

    return JsonResponse(bus_results_ser)


def get_ticket_status(request):
    """
    Получает статус билета из системы Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с информацией о статусе билета.
    """
    departure_id = '862fd93e-e633-11e7-80e7-00175d776a07'
    ticket_id = '01000000074024'
    vendor_id = ''

    client = get_client(WSDL_SALE)
    bus_results = client.service.GetTicketStatus(DepartureId=departure_id, TicketId=ticket_id, VendorId=vendor_id)
    bus_results_ser = serialize_object(bus_results)
    return JsonResponse(bus_results_ser)

# def get_directions(request):
#     url = "http://dev.avibus.pro/UEEDev/ws/SchedulePort?wsdl"
#     username = os.getenv('USER_NAME')
#     password = os.getenv('PASSWORD')
#
#     session = Session()
#     session.auth = HTTPBasicAuth(username, password)
#     client = Client(wsdl=url, transport=Transport(session=session))
#
#     bus_stops = client.service.GetBusStops()
#
#     travel_directions = [{'id': td.Id, 'name': td.Name} for td in bus_stops if td.Automated]
#     return render(request, 'base/home_page.html', {'travel_directions': travel_directions})
#
#
# def get_destinations(request):
#     url = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
#     username = os.getenv('USER_NAME')
#     password = os.getenv('PASSWORD')
#
#     session = Session()
#     session.auth = HTTPBasicAuth(username, password)
#     client = Client(wsdl=url, transport=Transport(session=session))
#
#     service = client.service
#     available_methods = service.__dir__()
#
#     # Вывод списка доступных методов
#     for method_name in available_methods:
#         print(method_name)
#
#     departure_id = request.POST.get('travel_direction')
#     departure_name = request.POST.get('travel_direction_name')
#     destinations = client.service.GetDestinations(Departure=departure_id, Substring='')
#
#     if destinations:
#         end_directions = [{'id': dis.Id, 'name': dis.Name} for dis in destinations]
#     else:
#         end_directions = None
#     context = {'end_directions': end_directions, 'departure': departure_id,
#                'departure_name': departure_name}
#     return render(request, 'base/search_bus.html', context=context)
#
#
# def search_results(request):
#     # Получение параметров запроса из GET-параметров
#     departure = request.POST.get('start_direction')
#     destination = request.POST.get('end_direction')
#     date = '2023-06-08'
#
#     # Логика вызова API и обработки результатов поиска
#     url = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
#     username = os.getenv('USER_NAME')
#     password = os.getenv('PASSWORD')
#
#     session = Session()
#     session.auth = HTTPBasicAuth(username, password)
#     client = Client(wsdl=url, transport=Transport(session=session))
#
#     bus_results = client.service.GetTrips(Departure=departure, Destination=destination, TripsDate=date)
#     bus_results_ser = serialize_object(bus_results)
#
#     # context = {'departure': departure, 'destination': destination, 'date': date, 'bus_results': bus_results_ser}
#     # print(type(bus_results))
#     # return render(request, 'base/search_results.html', context=context)
#     print(bus_results)
#     return JsonResponse(bus_results_ser)
#     # return HttpResponse(bus_results_ser)
#
#
# def search_trip_segment(request):
#     # Получение параметров запроса из GET-параметров
#     departure = 'cb654d84-f487-11ed-83c7-d00da3a6c886'
#     destination = '862fd93e-e633-11e7-80e7-00175d776a07'
#     trip_id = '38871dbb-dffe-11e7-80e7-00175d776a078ef8b472-fcd3-11ed-0591-d00d5ddf9041'
#
#     # Логика вызова API и обработки результатов поиска
#     url = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
#     username = os.getenv('USER_NAME')
#     password = os.getenv('PASSWORD')
#
#     session = Session()
#     session.auth = HTTPBasicAuth(username, password)
#     client = Client(wsdl=url, transport=Transport(session=session))
#
#     bus_results = client.service.GetTripSegment(TripId=trip_id, Departure=departure, Destination=destination)
#     bus_results_ser = serialize_object(bus_results)
#     print(bus_results)
#     return JsonResponse(bus_results_ser)
#
#
# def get_occupied_seats(request):
#     # Получение параметров запроса из GET-параметров
#     departure = 'cb654d84-f487-11ed-83c7-d00da3a6c886'
#     destination = '862fd93e-e633-11e7-80e7-00175d776a07'
#     trip_id = '38871dbb-dffe-11e7-80e7-00175d776a078ef8b472-fcd3-11ed-0591-d00d5ddf9041'
#     order_id = ''
#
#     # Логика вызова API и обработки результатов поиска
#     url = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
#     username = os.getenv('USER_NAME')
#     password = os.getenv('PASSWORD')
#
#     session = Session()
#     session.auth = HTTPBasicAuth(username, password)
#     client = Client(wsdl=url, transport=Transport(session=session))
#
#     bus_results = client.service.GetOccupiedSeats(TripId=trip_id, Departure=departure,
#                                                   Destination=destination, OrderId=order_id)
#     bus_results_ser = serialize_object(bus_results)
#     print(bus_results)
#     return JsonResponse(bus_results_ser)
#
#
# def start_sale_session(request):
#     # Получение параметров запроса из GET-параметров
#     departure = 'cb654d84-f487-11ed-83c7-d00da3a6c886'
#     destination = '862fd93e-e633-11e7-80e7-00175d776a07'
#     trip_id = '38871dbb-dffe-11e7-80e7-00175d776a078ef8b472-fcd3-11ed-0591-d00d5ddf9041'
#     order_id = ''
#
#     # Логика вызова API и обработки результатов поиска
#     url = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
#     username = os.getenv('USER_NAME')
#     password = os.getenv('PASSWORD')
#
#     session = Session()
#     session.auth = HTTPBasicAuth(username, password)
#     client = Client(wsdl=url, transport=Transport(session=session))
#
#     bus_results = client.service.StartSaleSession(TripId=trip_id, Departure=departure,
#                                                   Destination=destination, OrderId=order_id)
#     bus_results_ser = serialize_object(bus_results)
#     print(bus_results)
#     return JsonResponse(bus_results_ser)
#
#
# def add_tickets(request):
#     # Получение параметров запроса из GET-параметров
#     order_id = '00000026685'
#
#     ticket_seats = {
#         'Elements': {
#             'FareName': 'Багажный',
#             'SeatNum': '0',
#             'ParentTicketSeatNum': '0'
#         }
#     }
#
#     # Логика вызова API и обработки результатов поиска
#     url = "http://dev.avibus.pro/UEEDev/ws/SalePort?wsdl"
#     username = os.getenv('USER_NAME')
#     password = os.getenv('PASSWORD')
#
#     session = Session()
#     session.auth = HTTPBasicAuth(username, password)
#     client = Client(wsdl=url, transport=Transport(session=session))
#
#     bus_results = client.service.AddTickets(OrderId=order_id, TicketSeats=ticket_seats)
#     bus_results_ser = serialize_object(bus_results)
#     print(bus_results)
#     return JsonResponse(bus_results_ser)
