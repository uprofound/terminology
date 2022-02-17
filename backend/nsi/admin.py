from django.contrib import admin

from .models import Catalog, CatalogContent, CatalogVersion


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'version_count')
    list_filter = ('id', 'short_name')
    search_fields = ('name', 'description')

    @admin.display(description='Кол-во версий',)
    def version_count(self, obj):
        return CatalogVersion.objects.filter(catalog=obj).count()


class CatalogVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'catalog', 'version', 'start_date')
    list_filter = ('catalog', 'version', 'start_date')


class CatalogContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'catalog_version', 'code', 'value')
    list_filter = ('catalog_version', 'code', 'value')


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(CatalogVersion, CatalogVersionAdmin)
admin.site.register(CatalogContent, CatalogContentAdmin)
