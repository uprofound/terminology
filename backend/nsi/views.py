from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Catalog, CatalogContent, CatalogVersion
from .schemas import (CATALOG_CONTENT_PARAMS, CATALOG_LIST_PARAMS,
                      CATALOG_RETRIEVE_PARAMS, ITEM_VALIDATE_PARAMS,
                      catalogs_200, catalogs_id_200, catalogs_id_content_200)
from .serializers import (CatalogContentSerializer, CatalogSerializer,
                          CatalogVersionShowSerializer)
from .utils import get_catalog_version_for_date


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description='Получение списка справочников.',
        manual_parameters=CATALOG_LIST_PARAMS,
        responses={
            200: openapi.Response(
                description='',
                schema=CatalogSerializer,
                examples={
                    'application/json': catalogs_200
                },
            ),
        }
    ),
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_description='Просмотр информации о версии справочника.',
        manual_parameters=CATALOG_RETRIEVE_PARAMS,
        responses={
            200: openapi.Response(
                description='',
                schema=CatalogVersionShowSerializer,
                examples={
                    'application/json': catalogs_id_200
                },
            ),
        }
    )
)
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
        """ Находим актуальную (на текущую дату) версию справочника,
        либо версию, указанную в параметре version.
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
            return CatalogVersionShowSerializer
        return CatalogSerializer

    @swagger_auto_schema(
        manual_parameters=ITEM_VALIDATE_PARAMS,
        responses={
            200: 'Успешная валидация элемента справочника '
                 'по коду [и значению].',
            400: 'Некорректный запрос, например, не передан '
                 'code - обязательный параметр валидации.',
            404: 'Элемент справочника с кодом "code" '
                 '[и значением "value"] не найден.'
        }
    )
    @action(detail=True)
    def validate(self, *args, **kwargs):
        """ Валидация элемента заданного справочника по коду [и значению]
        в текущей версии справочника, либо переданной в параметре version.
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


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description=('Получение элементов заданного справочника '
                               'текущей (или указанной) версии.'),
        manual_parameters=CATALOG_CONTENT_PARAMS,
        responses={
            200: openapi.Response(
                description='',
                schema=CatalogContentSerializer,
                examples={
                    'application/json': catalogs_id_content_200
                },
            ),
        }

    )
)
class CatalogContentView(ListAPIView):
    serializer_class = CatalogContentSerializer

    def get_queryset(self):
        """ Формируем содержимое текущей версии указанного справочника,
        либо версии, указанной в параметре version.
        """
        catalog_id = self.kwargs.get('id')
        version = self.request.query_params.get('version')
        if version:
            catalog_version = get_object_or_404(
                CatalogVersion,
                catalog_id=catalog_id,
                version=version
            )
        else:
            # находим версию справочника, актуальную на текущую дату
            catalog_version = get_catalog_version_for_date(
                catalog_id,
                timezone.localdate()
            )
        return CatalogContent.objects.filter(catalog_version=catalog_version)
