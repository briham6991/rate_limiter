from django.contrib import admin
from core.models import CustomUser, PlanInformation, KeyInformation, KeyUtilizationInfo, CompanyInformation

admin.site.register(CustomUser)
admin.site.register(PlanInformation)
admin.site.register(CompanyInformation)
admin.site.register(KeyInformation)
admin.site.register(KeyUtilizationInfo)

# Register your models here.
