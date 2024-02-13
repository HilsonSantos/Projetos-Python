from django.contrib import admin
from .models import *


class CadClientesAdmin(admin.ModelAdmin):
    list_display = ('cpfcnpj', 'nrazaosocial')


admin.site.register(Clientes, CadClientesAdmin)
