from django.contrib import admin
from .models import *


admin.site.register(Car)
admin.site.register(Technique_model)
admin.site.register(Engine_model)
admin.site.register(Transmission_model)
admin.site.register(Drive_axle_model)
admin.site.register(Steerable_axle_model)
admin.site.register(Service_company)
admin.site.register(Type_maintenance)
admin.site.register(Maintenance)
admin.site.register(Description_failure)
admin.site.register(Recovery_method)
admin.site.register(Complaints)