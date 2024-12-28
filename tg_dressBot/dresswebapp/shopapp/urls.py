from django.urls import path
from . import views

urlpatterns = [
       path('', name='index'), # Добавили шаблон для корневого URL
       path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
   ]

