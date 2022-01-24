from django.contrib import admin

# Register your models here.
from crm.models import Client, Contract, Event

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
