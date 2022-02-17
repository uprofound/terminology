from rest_framework import serializers

from .models import Catalog, CatalogContent, CatalogVersion
from .utils import get_catalog_version_for_date


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
        request = self.context.get('request')
        actual_date = request.query_params.get('actual_date')
        if actual_date:
            version = get_catalog_version_for_date(catalog, actual_date)
            return CatalogVersionSerializer(version).data
        versions = CatalogVersion.objects.filter(catalog=catalog)
        return CatalogVersionSerializer(versions, many=True).data


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogContent
        fields = ('code', 'value')


class CatalogContentSerializer(serializers.ModelSerializer):
    short_name = serializers.ReadOnlyField(source='catalog.short_name')
    elements = serializers.SerializerMethodField()

    class Meta:
        model = CatalogVersion
        fields = (
            'catalog', 'short_name', 'version', 'start_date', 'elements'
        )

    def get_elements(self, catalog_version):
        content = CatalogContent.objects.filter(
            catalog_version=catalog_version
        )
        return ContentSerializer(content, many=True).data
