from django.contrib import admin

from flats.models import Flat


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    """
    Административный интерфейс управления объектами квартир
    """

    pass
