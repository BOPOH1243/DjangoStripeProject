from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import Item
import stripe
from decimal import Decimal

def item_detail(request, id):
    item = get_object_or_404(Item, pk=id)
    context = {
        'item': item,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'shop/item.html', context)

def buy_item(request, id):
    item = get_object_or_404(Item, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    unit_amount = int(Decimal(item.price) * 100)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': unit_amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success?session_id={CHECKOUT_SESSION_ID}'),
        cancel_url=request.build_absolute_uri('/cancel'),
    )
    return JsonResponse({'id': session.id})

def success(request):
    """
    Отображает страницу успешной оплаты. 
    Идентификатор сессии передается в GET-параметре session_id.
    """
    session_id = request.GET.get('session_id')
    return render(request, 'shop/success.html', {'session_id': session_id})

def cancel(request):
    """
    Отображает страницу, если оплата была отменена.
    """
    return render(request, 'shop/cancel.html')
