"""
inventory/models.py
"""
from django.db import models
from django.contrib.auth.models import User

from djge.models import UltraModel


class Container(UltraModel):
    name = models.CharField(max_length=64, unique=False, default='')
    size = models.SmallIntegerField(default=1)
    contents = models.ManyToManyField('Item', null=True, blank=True)


class Attribute(UltraModel):
    name = models.CharField(max_length=64, unique=True)


class Enchant(UltraModel):
    name = models.ForeignKey('Attribute', related_name='enchant')
    value = models.IntegerField(default=0)


class BaseItem(UltraModel):
    """
    Global item templates
    """
    name = models.CharField(max_length=64, unique=True)
    cost = models.PositiveIntegerField(default=0)
    power = models.IntegerField(default=1)
    CHOICES = (
        ('20', 'Junk'),
        ('30', 'Regular'),
        ('40', 'Uncommon'),
        ('50', 'Rare'),
        ('60', 'Epic'),
        ('70', 'Legendary'),
    )
    quality = models.CharField(max_length=2, choices=CHOICES, default=CHOICES[0])
    enchant = models.ManyToManyField('Enchant', null=True, blank=True)
    CATEGORIES = (
        ('20', 'N/A'),
        ('30', 'offense'),
        ('40', 'defense'),
        ('50', 'special'),
    )
    category = models.CharField(max_length=2, choices=CATEGORIES, default=CATEGORIES[0])


class Item(UltraModel):
    """
    In use this is an Instance of BaseItem.
    """
    name = models.CharField(max_length=64, default='DEFAULT')
    base = models.ForeignKey('BaseItem')
    enchant = models.ManyToManyField('Enchant', null=True, blank=True)
    durability = models.SmallIntegerField(default=100)
