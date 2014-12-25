"""
djge/models.py
"""
from django.db import models


class UltraModel(models.Model):
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)


class Mob(UltraModel):
    level = models.PositiveIntegerField(default=1)
    life = models.PositiveIntegerField(default=1)
    life_max = models.PositiveIntegerField(default=1)
    mana = models.PositiveIntegerField(default=1)
    mana_max = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True