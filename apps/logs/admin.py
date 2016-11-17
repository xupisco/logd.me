from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from .models import LogKind, Log


class LogKindAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'name', 'c_usage', )
    prepopulated_fields = {'slug': ('name',)}

    def owner_name(self, obj):
        return obj.owner.get_full_name()
    owner_name.short_description = _('owner')

    def c_usage(self, obj):
        return obj.log_set.count()
    c_usage.short_description = _('usage')


class LogAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'kind', 'short_body', 'reminder', 'start_date', 'c_companies', 'c_people', )
    list_filter = ('reminder', )
    list_display_links = ('kind', )
    search_fields = ('body', 'companies__name', 'people__name', )

    def owner_name(self, obj):
        return obj.owner.get_full_name()
    owner_name.short_description = _('owner')

    def short_body(self, obj):
        body = strip_tags(obj.body)
        ml = 50
        return (body[:ml] + '...') if len(body) > ml else body
    short_body.allow_tags = True
    short_body.short_description = _('preview')

    def c_companies(self, obj):
        return obj.companies.count()
    c_companies.short_description = _('companies')

    def c_people(self, obj):
        return obj.people.count()
    c_people.short_description = _('people')


admin.site.register(LogKind, LogKindAdmin)
admin.site.register(Log, LogAdmin)
