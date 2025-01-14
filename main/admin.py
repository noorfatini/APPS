from django.contrib import admin
from . import models
# Register your models here.

class ProductionPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username',]

admin.site.register(models.ProductionPlan, ProductionPlanAdmin)