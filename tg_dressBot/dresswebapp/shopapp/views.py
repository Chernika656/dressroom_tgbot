from json import JSONDecodeError

from django.http import JsonResponse
from django.shortcuts import render
import re
from .models import WebDress # Импорт модели WebDress


def add_to_cart(request):
    """
    Обработчик POST-запроса для добавления товара в корзину.
    """
    if request.method == 'POST':
        try:
            # Получение данных из POST-запроса (предполагается формат JSON)
            data = request.body.decode('utf-8')
            import json
            data = json.loads(data) # Преобразуем строку в словарь Python

            user_id = data.get('userId')
            photo_id_str = data.get('photoId')
            selected_size = data.get('selectedSize')

            # Проверка на наличие всех необходимых данных
            if not user_id or not photo_id_str or not selected_size:
                return JsonResponse({'error': 'Не все данные предоставлены'}, status=400)

            # Извлечение 4 цифр из photo_id с помощью регулярного выражения
            match = re.search(r'\d{4}', photo_id_str)
            if not match:
                return JsonResponse({'error': 'Неверный формат photo_id'}, status=400)
            photo_id = match.group(0)

            # Создание объекта WebDress и сохранение в базу данных
            web_dress = WebDress(user_id=user_id, photo_id=photo_id, size=selected_size)
            web_dress.save()

            return JsonResponse({'message': 'Товар добавлен в корзину'})

        except JSONDecodeError:
            return JsonResponse({'error': 'Неверный формат JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) # Возвращаем ошибку сервера

    return JsonResponse({'error': 'Неверный метод запроса'}, status=405) # Возвращаем ошибку, если метод не POST