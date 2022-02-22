import json
import os

from django.conf import settings
from drf_yasg import openapi

CATALOG_LIST_PARAMS = [
    openapi.Parameter(
        'actual_date',
        openapi.IN_QUERY,
        description=('Дата, для получения списка справочников и '
                     'их версий, актуальных именно на эту дату.'),
        type=openapi.FORMAT_DATE
    )
]

CATALOG_RETRIEVE_PARAMS = [
    openapi.Parameter(
        'id',
        openapi.IN_PATH,
        description='Идентификатор справочника.',
        type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        'version',
        openapi.IN_QUERY,
        description=('Версия справочника для получения информации, '
                     'если не указана - выдаётся информация о '
                     'текущей версии указанного справочника, '
                     'актуальной на текущую дату.'),
        type=openapi.TYPE_STRING
    )
]

CATALOG_CONTENT_PARAMS = [
    openapi.Parameter(
        'id',
        openapi.IN_PATH,
        description='Идентификатор справочника.',
        type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        'version',
        openapi.IN_QUERY,
        description=('Версия справочника для получения его элементов, '
                     'если не указана - выдаётся содержимое текущей '
                     'версии запрашиваемого справочника, '
                     'актуальной на текущую дату.'),
        type=openapi.TYPE_STRING
    )
]

ITEM_VALIDATE_PARAMS = [
    openapi.Parameter(
        'id',
        openapi.IN_PATH,
        description='Идентификатор справочника.',
        type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        'code',
        openapi.IN_QUERY,
        required=True,
        description='Проверяемый код элемента',
        type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        'value',
        openapi.IN_QUERY,
        description='Проверяемое значение элемента',
        type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        'version',
        openapi.IN_QUERY,
        description=('Версия справочника для валидации элемента, '
                     'если не указана - валидация по текущей '
                     'версии указанного справочника, '
                     'актуальной на текущую дату.'),
        type=openapi.TYPE_STRING
    )
]


examples_dir = settings.BASE_DIR / 'nsi' / 'response_examples'

response_examples = {
    'catalogs_200': None,
    'catalogs_id_200': None,
    'catalogs_id_content_200': None,
}

for example in response_examples:
    try:
        file_path = examples_dir / (example + '.json')
        if os.path.isfile(file_path):
            with open(file_path, encoding='utf-8') as json_file:
                response_examples[example] = json.load(json_file)
    except Exception as exc:
        print(f'Ошибка при загрузке шаблона {file_path}: {exc}')
