# bin_service/bin_lookup/apps.py

from django.apps import AppConfig

class BinLookupConfig(AppConfig):
    name = 'bin_service.bin_lookup'
    verbose_name = 'Bin Lookup'

default_app_config = 'bin_service.bin_lookup.BinLookupConfig'
