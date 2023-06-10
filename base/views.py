import json
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .utils import *


def directions_view(request):
    """
    Получает список доступных направлений из системы Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с направлениями.
    """
    if request.method == 'GET':
        directions = get_directions(request)
        return directions


def destinations_view(request):
    """
    Получает список пунктов назначения для выбранного направления из системы Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с пунктами назначения.
    """
    if request.method == 'GET':
        destinations = get_destinations(request)
        return JsonResponse(destinations)


@csrf_exempt
def search_trips_view(request):
    """
    Выполняет поиск поездок на основе выбранного направления и пункта назначения в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатами поиска.
    """
    # try:
    #     if request.method != 'POST':
    #         return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
    #     values = json.loads(request.body)
    #     # token = request.headers.get('Authorization')
    #     result = utl.search_trips(values=values)
    #
    #     return result
    # except Exception as ex:
    #     return HttpResponseBadRequest(f'Something goes wrong: {ex}')

    if request.method == 'GET':
        trips = search_trips(request)
        return JsonResponse(trips)


def trip_segment_view(request):
    """
    Получает информацию о выбранной поездке и сегментах поездки из системы Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с информацией о поездке и сегментах.
    """
    if request.method == 'GET':
        trip_segment = search_trip_segment(request)
        return JsonResponse(trip_segment)


def occupied_seats_view(request):
    """
    Получает информацию о занятых и свободных местах на выбранной поездке в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с информацией о местах.
    """
    if request.method == 'GET':
        occupied_seats = get_occupied_seats(request)
        return JsonResponse(occupied_seats)


def start_sale_session_view(request):
    """
    Начинает сессию продажи билетов для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом начала сессии продажи.
    """
    if request.method == 'POST':
        result = start_sale_session(request)
        return JsonResponse(result)


def add_tickets_view(request):
    """
    Добавляет билеты в заказ для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом добавления билетов в заказ.
    """
    if request.method == 'POST':
        result = add_tickets(request)
        return JsonResponse(result)


def add_tickets_baggage_view(request):
    """
    Добавляет билеты для багажа в заказ для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом добавления билетов для багажа в заказ.
    """
    if request.method == 'POST':
        result = add_tickets_baggage(request)
        return JsonResponse(result)


def del_tickets_view(request):
    """
    Удаляет билеты в заказ для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом удаления билетов из заказа.
    """
    if request.method == 'POST':
        result = del_tickets(request)
        return JsonResponse(result)


@csrf_exempt
def change_fare_name_view(request: HttpRequest):
    """
    Смена тарифа для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом изменения тарифа в заказе.
    """
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        # token = request.headers.get('Authorization')
        result = change_fare_name(values)

        return JsonResponse(result)
    except Exception as ex:
        return HttpResponseBadRequest(f'Something goes wrong: {ex}')
    # if request.method == 'POST':
    #     result = change_fare_name(request)
    #     return JsonResponse(result)


@csrf_exempt
def set_ticket_data_view(request):
    """
    Заполнение данных в билетах для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом добавления данных для поездки.
    """
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        # token = request.headers.get('Authorization')
        result = set_ticket_data(values)

        return JsonResponse(result)
    except Exception as ex:
        return HttpResponseBadRequest(f'Something goes wrong: {ex}')
    # if request.method == 'POST':
    #     result = utl.set_ticket_data(request)
    #     return JsonResponse(result)


@csrf_exempt
def reserve_order_view(request):
    """
    Бронирование заказа для оплаты в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом бронирования заказа.
    """
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        # token = request.headers.get('Authorization')
        result = reserve_order(values)

        return JsonResponse(result)
    except Exception as ex:
        return HttpResponseBadRequest(f'Something goes wrong: {ex}')
    # if request.method == 'POST':
    #     result = utl.reserve_order(request)
    #     return JsonResponse(result)


@csrf_exempt
def make_payment_view(request):
    """
    Оплата заказа для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом оплаты заказа.
    """
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        # token = request.headers.get('Authorization')
        result = make_payment(values)

        return JsonResponse(result)
    except Exception as ex:
        return HttpResponseBadRequest(f'Something goes wrong: {ex}')
    # if request.method == 'POST':
    #     result = utl.make_payment(request)
    #     return JsonResponse(result)


def cancel_payment_view(request):
    """
           Отмена оплата заказа для выбранной поездки в системе Avibus.
           Метод используется для отмены оплаты в случае технических проблем.
           Вызвать его можно только в течение 10 минут после вызова метода Payment.

           Args:
               request (HttpRequest): Запрос Django.

           Returns:
               JsonResponse: JSON-ответ с результатом отмены оплаты заказа.
           """
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        # token = request.headers.get('Authorization')
        result = cancel_payment(values)

        return JsonResponse(result)
    except Exception as ex:
        return HttpResponseBadRequest(f'Something goes wrong: {ex}')
    # if request.method == 'POST':
    #     result = utl.cancel_payment(request)
    #     return JsonResponse(result)


def create_return_order_view(request):
    """
    Создает заказ на возврат билета в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом создания заказа на возврат.
    """
    if request.method == 'POST':
        result = create_return_order(request)
        return JsonResponse(result)


def add_ticket_return_view(request):
    """
    Добавляет билет для возврата в заказ для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом добавления билета для возврата в заказ.
    """
    if request.method == 'POST':
        result = add_ticket_return(request)
        return JsonResponse(result)


def delete_ticket_return_view(request):
    """
    Удаляет билет из возврата в заказе для выбранной поездки в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом удаления билета из возврата в заказе.
    """
    if request.method == 'POST':
        result = delete_ticket_return(request)
        return JsonResponse(result)


def return_payment_view(request):
    """
    Возвращает заказ в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом возврата заказа.
    """
    if request.method == 'POST':
        result = return_payment(request)
        return JsonResponse(result)


def cancel_return_payment_view(request):
    """
    Отменяет возврат заказа в системе Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с результатом отмены возврата заказа.
    """
    if request.method == 'POST':
        result = cancel_return_payment(request)
        return JsonResponse(result)


def get_ticket_status_view(request):
    """
    Получает статус билета из системы Avibus.

    Args:
        request (HttpRequest): Запрос Django.

    Returns:
        JsonResponse: JSON-ответ с информацией о статусе билета.
    """
    if request.method == 'GET':
        result = get_ticket_status(request)
        return JsonResponse(result)
