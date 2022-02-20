import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from nsi.models import Catalog, CatalogContent, CatalogVersion


class Command(BaseCommand):
    help = 'Команда для импорта данных из csv-файлов в БД.'

    def handle(self, *args, **kwargs):
        # директория с загружаемыми файлами данных относительно BASE_DIR
        data_dir = os.path.join('nsi', 'data')
        # имена файлов должны быть в формате:
        # <короткое наименование справочника>_<версия>_ГГГГ-ММ-ДД.csv,
        # где ГГГГ-ММ-ДД - дата начала действия справочника этой версии
        for file in os.listdir(data_dir):
            try:
                # получаем атрибуты справочника из названия файла
                short_name, version, start_date = file[:-4].split('_')
                # считываем элементы справочника из файла
                with open(
                        os.path.join(data_dir, file),
                        encoding='utf-8'
                ) as csv_file:
                    content_data = list(csv.reader(csv_file, delimiter=';'))

                with transaction.atomic():
                    # получаем или создаём справочник
                    catalog, _ = Catalog.objects.get_or_create(
                        name=short_name,
                        short_name=short_name
                    )
                    # получаем или создаём версию справочника
                    catalog_version, _ = CatalogVersion.objects.get_or_create(
                        catalog=catalog,
                        version=version,
                        start_date=start_date
                    )
                    # обновляем элементы справочника
                    for row in content_data:
                        code, value = row
                        CatalogContent.objects.get_or_create(
                            catalog_version=catalog_version,
                            code=code,
                            value=value
                        )
            except Exception as exc:
                self.stdout.write(self.style.ERROR(
                    f'Ошибка во время загрузки данных: {exc}'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Данные из {file} загружены.'
                ))
