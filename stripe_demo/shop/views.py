import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def item_detail(request, id):
    item = get_object_or_404(Item, pk=id)
    context = {
        'item': item,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'shop/item_detail.html', context)

def buy_item(request, id):
    """Создаёт Stripe Checkout Session для одиночного товара"""
    item = get_object_or_404(Item, pk=id)
    domain = request.build_absolute_uri('/')[:-1]  # Убираем завершающий слеш
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * Decimal('100')),  # цена в центах
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def catalog(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'shop/catalog.html', context)

def add_to_order(request, id):
    """Добавляет выбранный товар в заказ, связанный с сессией пользователя"""
    item = get_object_or_404(Item, pk=id)
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    order, created = Order.objects.get_or_create(session_key=session_key)
    order.items.add(item)
    return redirect('order_detail')

def order_detail(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    order = Order.objects.filter(session_key=session_key).first()
    context = {
        'order': order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'shop/order_detail.html', context)

def create_payment_intent(request):
    """Создаёт Payment Intent для оплаты всего заказа (бонус – PaymentIntent)"""
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    order = Order.objects.filter(session_key=session_key).first()
    if not order or order.items.count() == 0:
        return JsonResponse({'error': 'Order is empty.'}, status=400)
    currency = order.order_currency()
    total = order.total_amount()
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(total * Decimal('100')),
            currency=currency,
            metadata={'order_id': order.id}
        )
        return JsonResponse({'client_secret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def success(request):
    return render(request, 'shop/success.html')

def cancel(request):
    return render(request, 'shop/cancel.html')
