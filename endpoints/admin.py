from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Categories)
admin.site.register(models.SubCategories)
admin.site.register(models.SubSubCategories)
