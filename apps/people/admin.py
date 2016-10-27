from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Role, Person


class RoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'mobile', 'company', )
    list_filter = ('role', 'company', )
    search_fields = ('name', 'role__name', 'company__name', )


admin.site.register(Role, RoleAdmin)
admin.site.register(Person, PersonAdmin)