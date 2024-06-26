from django.contrib import admin
from .models import Store, Clothes, Selfie

# Register your models here.
admin.site.register(Store)
admin.site.register(Clothes)
admin.site.register(Selfie)