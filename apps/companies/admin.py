from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Company, CompanyAdmin)