from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Bearer

@admin.register(Bearer)
class BearerAdmin(ImportExportModelAdmin):
    pass