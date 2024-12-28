from django.db import models

class WebDress(models.Model):
    """
    Модель для хранения информации о товарах в корзине.
    """
    user_id = models.IntegerField() # ID пользователя
    photo_id = models.CharField(max_length=4) # ID фотографии (4 цифры)
    size = models.IntegerField() # Размер

    def __str__(self):
        return f"Товар: user_id={self.user_id}, photo_id={self.photo_id}, size={self.size}"