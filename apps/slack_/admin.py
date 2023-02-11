from django.contrib import admin

from .models import (
    SlackFile,
    SlackMessage,
)


@admin.register(SlackFile)
class SlackFileAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(SlackMessage)
class SlackMessageAdmin(admin.ModelAdmin):
    pass
