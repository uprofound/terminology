from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Catalog, CatalogContent, CatalogVersion
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

    @action(detail=True)
    def validate(self, *args, **kwargs):
        """ Валидация элементов заданного справочника по коду
        (и, опционально, значению).
        Версия справочника определяется по переданной в качестве параметра
        запроса 'version', иначе - берём актуальную на текущую дату.
        """
        # проверяем, что передан обязательный параметр валидации
        code = self.request.query_params.get('code')
        if not code:
            return Response(
                {'Не передан code - обязательный параметр валидации.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # получаем экземпляр справочника элемент которого проверяем
        try:
            catalog_version = self.get_object(self)
        except Http404:
            return Response(
                {'id справочника или его версия заданы некорректно.'},
                status=status.HTTP_404_NOT_FOUND
            )
        # получаем значение элемента, если его тоже передали на проверку
        value = self.request.query_params.get('value')

        # валидируем элемент по переданным параметрам
        if value:
            try:
                get_object_or_404(
                    CatalogContent,
                    catalog_version=catalog_version,
                    code=code,
                    value=value
                )
            except Http404:
                return Response(
                    {(f"Элемент справочника с кодом '{code}' "
                      f"и значением '{value}' не найден.")},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                return Response(
                    {'Успешная валидация элемента справочника '
                     'по коду и значению.'},
                    status=status.HTTP_200_OK
                )
        try:
            get_object_or_404(
                CatalogContent,
                catalog_version=catalog_version,
                code=code
            )
        except Http404:
            return Response(
                {f"Элемент справочника с кодом '{code}' не найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(
                {'Успешная валидация элемента справочника по коду.'},
                status=status.HTTP_200_OK
            )
