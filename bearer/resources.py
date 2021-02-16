from django.contrib import admin
from import_export import resources
from .models import Bearer

class BearerResource(resources.ModelResource):
    class Meta:
        model = Bearer
