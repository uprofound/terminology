from django.db.models import Max
from django.shortcuts import get_object_or_404

from .models import CatalogVersion


def get_catalog_version_for_date(catalog, date):
    # находим максимальную дату начала действия справочника <= переданной
    actual_set = CatalogVersion.objects.values('catalog').filter(
        catalog=catalog,
        start_date__lte=date
    ).annotate(start_date=Max('start_date'))
    # возвращаем версию справочника, соответствующую
    # этой дате, если она существует
    return get_object_or_404(
        CatalogVersion,
        catalog=catalog,
        start_date=actual_set[0].get('start_date') if actual_set else None
    )
