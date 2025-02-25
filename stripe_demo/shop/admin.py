from django.contrib import admin
from .models import Item 

# Класс для настройки отображения модели в админке
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # поля, отображаемые в списке
    search_fields = ('name',)         # поля для поиска
    list_filter = ('price',)          # фильтры справа

# Регистрируем модель и ее настройки
admin.site.register(Item, ItemAdmin)