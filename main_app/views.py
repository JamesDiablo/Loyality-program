from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Card, Order, Item, Basket
from .forms import CardSearch_Form, Generator_Form
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CardSerializer, OrderSerializer, CardOrderSerializer, OrderItemSerializer
import datetime as dt
import pytz


class CardInfoView(generics.RetrieveAPIView):
    """
    Retrieves information about a card given its series and number.
    
    Returns:
        A serialized representation of the card information.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_object(self):
        series = self.kwargs['series']
        number = self.kwargs['number']
        if number is not None and series is not None:
            return self.queryset.get(number=number, series=series)
        raise Http404

class OrderCreateView(generics.CreateAPIView):
    """
    Creates an order for a given card.
    
    Returns:
        A serialized representation of the created order.
    """
    serializer_class = OrderSerializer

class OrderListByCard(generics.ListAPIView):
    """
    Lists all orders for a given card, filtered by date if specified.
    
    Returns:
        A serialized representation of the list of orders.
    """
    serializer_class = CardOrderSerializer

    def get_queryset(self):
        series = self.kwargs['series']
        number = self.kwargs['number']
        date = self.kwargs.get('date', None)

        card = Card.objects.get(series=series, number=number)

        if date:
            orders = card.orders.filter(date__contains=date)
        else:
            orders = card.orders.all()

        order_serialized = CardOrderSerializer(orders, many=True)
        
        for order in order_serialized.data:
            items = Item.objects.filter(order=order['id_order'])
            items_serialized = OrderItemSerializer(items, many=True)
            
            order['items'] = [item for item in items_serialized.data if item['order'] == order['id_order']]
        

        return order_serialized.data
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)

def index(request):
    """
    Function to generating main page and `CardSearch_Form` handler, which displays and processes a form.
    :param request: The incoming http request object.
    :return: rendered html template
    """
    form = CardSearch_Form(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        cards = Card.objects.filter(
            Q(series__contains=query) | 
            Q(number__contains=query) | 
            Q(release_date__contains=query) |
            Q(expire_date__contains=query) |
            Q(status__contains=query)
        )
    else:
        cards = Card.objects.all().order_by('id')

    context = {
        'title': 'Main page',
        'form': form, 
        'cards': cards
    }
    return render(request, 'index.html', context)


def card_info(request, series, number):
    """
    Function to generating template for card info page, which contains card and its orders objects.
    :param request: The incoming http request object.
    :param series: Get the card series passed in the URL.
    :param number: Get the card number passed in the URL.
    :return: rendered html template
    """
    card = get_object_or_404(Card, series=series, number=number)

    orders = card.orders.all()
    context = {
        'title': 'Card info',
        'card': card,
        'orders': orders
    }
    return render(request, 'card_info.html', context)

def order_info(request, id_order):
    """
    Function to generating template for order info page, which contains order and its items objects.
    :param request: The incoming http request object.
    :param id_order: Get the order id passed in the URL.
    :return: rendered html template
    """
    order = get_object_or_404(Order, id_order=id_order)
    order.total = order.sum-order.discount_calculation
    items = Item.objects.filter(order=order)
    
    context = {
        'title': 'Order info',
        'order': order,
        'items': items
    }
    return render(request, 'order.html', context)

def generator(request):
    """
    A function that processes the POST form to generate cards
    :param request: The incoming http request object.
    :return: rendered html template with success or error message
    """
    if request.method == 'POST':
        form = Generator_Form(request.POST)
        if form.is_valid():
            series = form.cleaned_data['series']
            timezone = pytz.timezone(settings.TIME_ZONE)
            start_date = timezone.localize(dt.datetime.combine(form.cleaned_data['start_date'], dt.datetime.min.time()))
            end_date = timezone.localize(dt.datetime.combine(form.cleaned_data['end_date'], dt.datetime.min.time()))
            cards = [Card(series=series, 
                          number=number,
                          release_date=start_date,
                          expire_date=end_date,
                          status='Inactive') for number in generate_card_numbers(form.cleaned_data['count'])]
            Card.objects.bulk_create(cards)
            messages.success(request, f'{form.cleaned_data["count"]} карт лояльности было успешно создано!')
    else:
        form = Generator_Form()
    
    context = {
        'title': 'Generator',
        'form': form
    }
    return render(request, 'generator.html', context)

def generate_card_numbers(count):
    """
    Function to generate unique card numbers. In the loop, we generate the card number and fill in the string up to 16 characters
    :param count: Number of cards to generate.
    :return: list of card numbers
    """
    card_numbers = []
    for i in range(1, count+1):
        card_number = str(i).zfill(16)
        card_numbers.append(card_number)
    return card_numbers

def action(request, series, number):
    """
    Function to activate/deactivate the card
    :param request: The incoming http request object.
    :param series: Get the card series passed in the URL.
    :param number: Get the card number passed in the URL.
    :return: rendered html template
    """
    card = get_object_or_404(Card, series=series, number=number)
    
    status = "Inactive" if card.status == "Active" else "Active"
    card.status = status
    card.save()

    orders = card.orders.all()
    context = {
        'title': 'Card info',
        'card': card,
        'orders': orders
    }
    return render(request, 'card_info.html', context)

def delete_card(request, series, number):
    """
    Function to delete/restoring the card.
    :param request: The incoming http request object.
    :param series: Get the card series passed in the URL.
    :param number: Get the card number passed in the URL.
    :return: redirect to main page
    """
    card = Card.objects.get(series=series, number=number)
    
    if card.deleted == False:
        card.deleted = True
        basket = Basket(card=card)
        basket.save()
    else:
        card.deleted = False
        basket = Basket.objects.get(card=card)
        basket.delete()

    card.save()
    return redirect('index')

def basket(request):
    """
    Function to generating template for basket page and `CardSearch_Form` handler, which displays and processes a form.
    :param request: The incoming http request object.
    :return: rendered html template
    """
    form = CardSearch_Form(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        print(query)
        basket_cards = Basket.objects.filter(
            Q(card__series__contains=query) |
            Q(card__number__contains=query) |
            Q(card__release_date__contains=query) |
            Q(card__expire_date__contains=query) |
            Q(card__status__contains=query)
        )
    else:
        basket_cards = Basket.objects.all().order_by('id')

    context = {
        'title': 'Basket',
        'form': form, 
        'basket_cards': basket_cards
    }
    return render(request, 'basket.html', context)

def error_404_view(request, exception):
    """
    Function for custom error page template
    :param request: The incoming http request object.
    :param request: Exception
    :return: rendered html 404 template
    """
    return render(request, '404.html', status=404)