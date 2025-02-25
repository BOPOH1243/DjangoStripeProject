from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>', views.item_detail, name='item_detail'),
    path('buy/<int:id>', views.buy_item, name='buy_item'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
]
