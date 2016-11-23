from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'owner_name', )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('owner__first_name', 'owner__last_name', 'name', )

    def owner_name(self, obj):
        return obj.owner.get_full_name()
    owner_name.short_description = _('owner')


admin.site.register(Company, CompanyAdmin)
