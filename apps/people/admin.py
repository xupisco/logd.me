from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Role, Person


class RoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PersonAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'name', 'email', 'role', 'mobile', 'company', )
    list_filter = ('role', 'company', )
    search_fields = ('name', 'role__name', 'company__name', )
    list_display_links = ('name', )

    def owner_name(self, obj):
        return obj.owner.get_full_name()
    owner_name.short_description = _('owner')


admin.site.register(Role, RoleAdmin)
admin.site.register(Person, PersonAdmin)
