from django.db import models

from apps.dlp.models import BaseMessage


class SlackFile(models.Model):
    file = models.FileField(verbose_name='File')
    filetype = models.CharField(max_length=255, verbose_name='File Type')
    filename = models.CharField(max_length=255, verbose_name='File Name')

    def __str__(self):
        return f'{self.id} - {self.filename}'


class SlackMessage(BaseMessage):
    team_id = models.CharField(max_length=255, verbose_name='Team ID')
    channel_id = models.CharField(max_length=255, verbose_name='Channel ID')
    owner_id = models.CharField(max_length=255, verbose_name='User ID')

    files = models.ManyToManyField(
        SlackFile,
        related_name='messages',
        verbose_name='Files',
    )

    def __str__(self):
        return f'{self.id} - {self.channel_id}'
