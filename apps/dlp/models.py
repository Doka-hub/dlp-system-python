from django.db import models


class ReTemplate(models.Model):
    pattern = models.TextField(verbose_name='Regex Pattern')

    @property
    def rpattern(self):
        return fr'{self.pattern}'

    def __str__(self):
        return f'{self.id} - {self.pattern}'


class BaseMessage(models.Model):
    re_templates = models.ManyToManyField(
        ReTemplate,
        related_name='messages',
        verbose_name='Re Templates',
    )

    text = models.TextField(null=True, blank=True, verbose_name='Text')
    date = models.DateField(verbose_name='Date')
    time = models.TimeField(verbose_name='Time')

    class Meta:
        abstract = True
