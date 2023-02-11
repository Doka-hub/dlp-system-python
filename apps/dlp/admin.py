from django.contrib import admin

from .models import ReTemplate


@admin.register(ReTemplate)
class ReTemplateAdmin(admin.ModelAdmin):
    pass
