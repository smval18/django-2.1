from django.contrib import admin

from . import models


admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Status)
admin.site.register(models.Application)

