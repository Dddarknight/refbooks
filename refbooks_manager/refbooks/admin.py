from django.contrib import admin
from refbooks_manager.refbooks.models import RefBook, Version, Element


class RefbookAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description')


class ElementInline(admin.TabularInline):
    model = Element
    extra = 0


class VersionAdmin(admin.ModelAdmin):
    list_display = ('refbook', 'version', 'start_date')
    inlines = [
        ElementInline,
    ]


class ElementAdmin(admin.ModelAdmin):
    list_display = ('version', 'code', 'value')


admin.site.register(RefBook, RefbookAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Element, ElementAdmin)
