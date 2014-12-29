"""
mobile/models.py
"""
from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from djge.models import UltraModel

from world.models import Location
from inventory.models import Item


class Species(UltraModel):
    name = models.CharField(max_length=64)
    playable = models.BooleanField(default=False)
    starting_zone = models.ForeignKey(Location, null=True, blank=True)
    starting_hp = models.PositiveSmallIntegerField(default=1)
    starting_mp = models.PositiveSmallIntegerField(default=1)  # Values from 0 to 32767


class Gender(UltraModel):
    name = models.CharField(max_length=64)
    playable = models.BooleanField(default=False)


class BaseMobile(UltraModel):
    name = models.CharField(max_length=64)
    level = models.IntegerField(default=1)
    #
    life = models.IntegerField(default=1)
    life_max = models.IntegerField(default=1)
    #
    mana = models.IntegerField(default=1)
    mana_max = models.IntegerField(default=1)
    #
    species = models.ForeignKey('Species', null=True)
    gender = models.ForeignKey('Gender', null=True)
    #
    base_offense = models.IntegerField(default=1)
    #
    base_defense = models.IntegerField(default=1)

    class Meta:
        abstract = True


class PlayerCharacter(BaseMobile):
    user = models.ForeignKey(User)
    where = models.ForeignKey(Location)
    equip_offense = models.ForeignKey(Item, null=True, blank=True, related_name='pceqoff')
    equip_defense = models.ForeignKey(Item, null=True, blank=True, related_name='pceqdef')

    class Meta:
        unique_together = (('name', 'user'),)

    def get_absolute_url(self):
        return reverse('player:detail', kwargs={'pk': self.pk})

    def in_combat(self):
        try:
            this = self.battle_set.get()
        except ObjectDoesNotExist:
            return False
        if this.npcs.count() == 0:
            this.delete()
            return False
        return this


class NonPlayerCharacter(BaseMobile):
    spawns = models.ManyToManyField(Location, null=True, blank=True)
    CHOICE = (
        ('10',  'Friendly'),
        ('20',  'Neutral'),
        ('30',  'Hostile'),
        ('40',  'Invulnerable'),
    )
    attitude = models.CharField(max_length=2, choices=CHOICE, default=CHOICE[0][0])
