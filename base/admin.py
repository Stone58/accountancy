from django.contrib import admin

# Register your models here.
from .models import Operation, Company, OperationType

admin.site.register(Company)
admin.site.register(OperationType)
admin.site.register(Operation)