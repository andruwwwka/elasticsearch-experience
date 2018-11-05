from django.test import TestCase
from django.urls import reverse

from core.constants import Constants
from flats.models import Flat


class TestResources(TestCase):

    """
    Тесты ресурсов приложения квартир
    """

    @classmethod
    def setUpTestData(cls):
        super(TestResources, cls).setUpTestData()
        Flat.objects.create(
            room_count=Constants.APARTMENT_ROOM_COUNT_VALUE,
            price=1400000,
            area=25,
            balcony_type=Constants.BALCONY_BALCONY_TYPE,
            hypothec=True,
            military_hypothec=True
        )
        Flat.objects.create(
            room_count=Constants.TWO_ROOM_COUNT_VALUE,
            price=2850000,
            area=41,
            balcony_type=Constants.BALCONY_BALCONY_TYPE,
            hypothec=True,
            military_hypothec=False
        )
        Flat.objects.create(
            room_count=Constants.TWO_ROOM_COUNT_VALUE,
            price=4320000,
            area=72,
            balcony_type=Constants.LOGGIA_BALCONY_TYPE,
            hypothec=False,
            military_hypothec=True
        )

    def test_resource_update_unavailable(self):

        """
        Тест невозможности обновления данных о квартире через клиентский ресурс
        """
        flat = Flat.objects.last()
        response = self.client.put(
            reverse("flats-detail", args=(flat.id,))
        )
        self.assertEqual(response.status_code, 405)

    def test_resource_create_unavailable(self):
        """
        Тест недоступности создания объекта квартиры через клиентский ресурс
        """
        response = self.client.post(
            reverse("flats-list")
        )
        self.assertEqual(response.status_code, 405)

    def test_resource_delete_unavailable(self):
        """
        Тест недоступности удаления объекта квартиры через клиентский ресурс
        """
        flat = Flat.objects.last()
        response = self.client.delete(
            reverse("flats-detail", args=(flat.id,))
        )
        self.assertEqual(response.status_code, 405)

    def test_resource_detail(self):
        """
        Тест получения данных об отдельном объекте квартиры
        """
        flat = Flat.objects.last()
        response = self.client.get(
            reverse("flats-detail", args=(flat.id,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all([getattr(flat, key) == value for key, value in response.data.items()]))

    def test_resource_list(self):
        """
        Тест получения списка квартир
        """
        response = self.client.get(
            reverse("flats-list")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Flat.objects.count())
