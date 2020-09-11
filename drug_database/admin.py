from django.contrib import admin
from .models import ActiveComponent, Company, Product, DrugUse, SheepDrugType, SheepDrug, SheepPathogen


admin.site.register(ActiveComponent)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(DrugUse)
admin.site.register(SheepDrugType)
admin.site.register(SheepDrug)
admin.site.register(SheepPathogen)
