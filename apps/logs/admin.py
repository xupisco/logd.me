from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import LogKind, Log


class LogKindAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class LogAdmin(admin.ModelAdmin):
    list_display = ('kind', 'reminder', 'start_date', 'c_companies', 'c_people', )
    list_filter = ('reminder', )
    search_fields = ('body', 'companies__name', 'people__name', )

    def c_companies(self, obj):
        return obj.companies.count()
    c_companies.short_description = _('companies')

    def c_people(self, obj):
        return obj.people.count()
    c_people.short_description = _('people')


admin.site.register(LogKind, LogKindAdmin)
admin.site.register(Log, LogAdmin)