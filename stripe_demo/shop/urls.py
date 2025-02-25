from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('buy/<int:id>/', views.buy_item, name='buy_item'),
    path('catalog/', views.catalog, name='catalog'),
    path('add_to_order/<int:id>/', views.add_to_order, name='add_to_order'),
    path('order/', views.order_detail, name='order_detail'),
    path('order/create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
