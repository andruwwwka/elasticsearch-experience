from rest_framework.routers import SimpleRouter

from flats.resources import FlatListViewSet

router = SimpleRouter()

router.register("flats", FlatListViewSet, "flats")

urlpatterns = router.urls
