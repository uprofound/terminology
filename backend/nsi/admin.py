from django.contrib import admin

from .models import Catalog, CatalogContent, CatalogVersion


class CatalogVersionInline(admin.StackedInline):
    model = CatalogVersion
    extra = 1


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version_count')
    list_filter = ('id', 'short_name')
    search_fields = ('name', 'description')
    inlines = (CatalogVersionInline,)

    @admin.display(description='Кол-во версий',)
    def version_count(self, obj):
        return CatalogVersion.objects.filter(catalog=obj).count()


class CatalogContentInline(admin.StackedInline):
    model = CatalogContent
    extra = 3


@admin.register(CatalogVersion)
class CatalogVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'catalog', 'version', 'start_date')
    list_filter = ('catalog', 'version', 'start_date')
    inlines = (CatalogContentInline,)


@admin.register(CatalogContent)
class CatalogContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'catalog_version', 'code', 'value')
    list_filter = ('catalog_version',)
    search_fields = ('code', 'value')
