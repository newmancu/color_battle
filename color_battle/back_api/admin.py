from django.contrib import admin
from back_api import models


class AdminMapAction(admin.ModelAdmin):
  pass


class AdminCreators(admin.ModelAdmin):
  pass

class AdminMapBackUp(admin.ModelAdmin):
  pass

admin.site.register(models.MapAction, AdminMapAction)
admin.site.register(models.Creators, AdminCreators)
admin.site.register(models.MapBackUp, AdminMapBackUp)