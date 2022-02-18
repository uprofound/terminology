from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CatalogContentView, CatalogViewSet

router = DefaultRouter()
router.register('catalogs', CatalogViewSet, basename='catalogs')


urlpatterns = [
    path(
        'catalogs/<int:pk>/content/',
        CatalogContentView.as_view(),
        name='content'
    ),
    path('', include(router.urls)),
]
