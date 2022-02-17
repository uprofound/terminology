from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CatalogViewSet

router = DefaultRouter()
router.register('catalogs', CatalogViewSet, basename='catalogs')


urlpatterns = [
    path('', include(router.urls)),
]
