from django.db import models


class Catalog(models.Model):
    # здесь в качестве идентификатора - DEFAULT_AUTO_FIELD из settings,
    # возможно, лучше использовать models.UUIDField
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Наименование'
    )
    short_name = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Короткое наименование'
    )
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
        ordering = ['short_name']

    def __str__(self):
        return self.short_name


class CatalogVersion(models.Model):
    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='Справочник'
    )
    version = models.CharField(
        max_length=16,
        verbose_name='Версия'
    )
    start_date = models.DateField(
        verbose_name='Дата начала действия'
    )

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        constraints = [
            models.UniqueConstraint(
                fields=['catalog', 'version'],
                name='unique_catalog_version'
            ),
            models.UniqueConstraint(
                fields=['catalog', 'start_date'],
                name='unique_catalog_start_date'
            ),
            # запрещаем ввод пустой строки через прямой доступ к БД
            models.CheckConstraint(
                check=~models.Q(version=''),
                name='version_not_empty'
            )
        ]
        ordering = ['catalog', '-start_date']

    def __str__(self):
        return f'{self.catalog.id} ({self.version})'


class CatalogContent(models.Model):
    catalog_version = models.ForeignKey(
        CatalogVersion,
        on_delete=models.CASCADE,
        verbose_name='Версия справочника'
    )
    code = models.CharField(
        max_length=16,
        verbose_name='Код'
    )
    value = models.CharField(
        max_length=128,
        verbose_name='Значение'
    )

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(code=''),
                name='code_not_empty'
            ),
            models.CheckConstraint(
                check=~models.Q(value=''),
                name='value_not_empty'
            ),
            models.UniqueConstraint(
                fields=['catalog_version', 'code'],
                name='unique_catalog_version_code'
            )
        ]
        indexes = [
            models.Index(
                fields=['catalog_version', 'code'],
                name='catalog_version_code_idx'
            ),
        ]
        ordering = ['catalog_version', 'code']

    def __str__(self):
        return f'{self.catalog_version} - {self.code}'
