from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets

from .models import Catalog, CatalogVersion
from .serializers import CatalogContentSerializer, CatalogSerializer
from .utils import get_catalog_version_for_date


class CatalogViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        """ Формируем перечень справочников в зависимости от
        переданной/не переданной в качестве параметра запроса актуальной даты.
        """
        actual_date = self.request.query_params.get('actual_date')
        if actual_date:
            catalog_ids = CatalogVersion.objects.filter(
                start_date__lte=actual_date
            ).values_list('catalog_id', flat=True)
            return Catalog.objects.filter(id__in=catalog_ids)
        return Catalog.objects.all()

    def get_object(self, pk=None):
        """ Находим версию справочника в зависимости от указанной
        конкретной версии, если она передана в качестве параметра
        запроса 'version', иначе - актуальную на текущую дату.
        """
        pk = self.kwargs.get('pk')
        version = self.request.query_params.get('version')
        if not version:
            # возвращаем версию справочника, актуальную на текущую дату
            return get_catalog_version_for_date(pk, timezone.localdate())
        return get_object_or_404(
            CatalogVersion,
            catalog_id=pk,
            version=version
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CatalogContentSerializer
        return CatalogSerializer
