from pyexpat import model
from django.contrib import admin
from .models import Auth, Instruments, HistoricalData
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class HistoricalDataResource(resources.ModelResource):
    class Meta:
        model = HistoricalData


class HistoricalDataAdmin(ImportExportModelAdmin):
    resource_class = HistoricalDataResource


admin.site.register(HistoricalData, HistoricalDataAdmin)
