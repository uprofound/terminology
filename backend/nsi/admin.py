from django.contrib import admin

from .models import Catalog, CatalogContent, CatalogVersion

admin.site.register(Catalog)
admin.site.register(CatalogVersion)
admin.site.register(CatalogContent)
