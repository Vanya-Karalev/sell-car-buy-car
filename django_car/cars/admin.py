from django.contrib import admin
from cars.models import Brand, Model, Engine, Gearbox, Suspension, Car, Ad

admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Engine)
admin.site.register(Gearbox)
admin.site.register(Suspension)
admin.site.register(Car)
admin.site.register(Ad)
