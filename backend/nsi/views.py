from rest_framework import viewsets

from .models import Catalog, CatalogVersion
from .serializers import CatalogSerializer


class CatalogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CatalogSerializer

    def get_queryset(self):
        """ Формируем queryset в зависимости от переданной/не переданной
        в качестве параметра запроса актуальной даты.
        """
        actual_date = self.request.query_params.get('actual_date')
        if actual_date:
            catalog_ids = CatalogVersion.objects.filter(
                start_date__lte=actual_date
            ).values_list('catalog_id', flat=True)
            return Catalog.objects.filter(id__in=catalog_ids)
        return Catalog.objects.all()
