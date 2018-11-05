from django.core.validators import MinValueValidator
from django.db import models

from core.constants import Constants


class Flat(models.Model):
    """
    Модель для хранения информации о квартирах
    """

    room_count = models.CharField(
        'Комнатность',
        max_length=15,
        choices=((value, value) for value in Constants.ROOM_COUNT_VALUES)
    )
    price = models.IntegerField(
        'Цена',
        validators=[
            MinValueValidator(0, 'Цена не может быть отрицательной')
        ]
    )
    area = models.IntegerField(
        'Площадь',
        validators=[
            MinValueValidator(0, 'Площадь не может быть отрицательной')
        ]
    )
    balcony_type = models.CharField(
        'Тип балкона',
        max_length=30,
        choices=((value, value) for value in Constants.BALCONY_TYPES),
        blank=True,
        null=True
    )
    hypothec = models.BooleanField(
        'Ипотека',
        default=False
    )
    military_hypothec = models.BooleanField(
        'Военная ипотека',
        default=False
    )

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
