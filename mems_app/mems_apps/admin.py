from django.contrib import admin

# Register your models here.
from mems_apps.models import *

admin.site.register(MessExtra)
admin.site.register(Order)
# admin.site.register(Record)