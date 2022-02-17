from django.db.models import Max
from rest_framework import serializers

from .models import Catalog, CatalogVersion


class CatalogVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogVersion
        fields = ('version', 'start_date')


class CatalogSerializer(serializers.ModelSerializer):
    versions = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = ('id', 'name', 'short_name', 'description', 'versions')

    def get_versions(self, catalog):
        """ Формируем перечень версий справочника в зависимости от
        переданной/не переданной в качестве параметра запроса актуальной даты.
        """
        versions = CatalogVersion.objects.filter(catalog=catalog)

        request = self.context.get('request')
        actual_date = request.query_params.get('actual_date')
        if actual_date:
            # сначала находим максимальную дату начала
            # действия справочника ранее актуальной
            catalog_max_date = versions.values('catalog').filter(
                start_date__lte=actual_date
            ).annotate(start_date=Max('start_date'))

            if catalog_max_date:
                # оставляем только актуальную версию справочника
                versions = versions.filter(
                    catalog=catalog_max_date[0].get('catalog'),
                    start_date=catalog_max_date[0].get('start_date')
                )
            else:
                versions = []

        # если актуальная дата не передана - выдаются все версии справочника
        return CatalogVersionSerializer(versions, many=True).data
