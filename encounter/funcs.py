"""

"""
import random


def attack(self, attacker, target):
    if target.autoact('xtradodg'):
        return False
    base_damage = attacker.base_offense
    try:
        equipped_damage = attacker.equip_offense.base.power
    except:
        equipped_damage = 0
    total_damage = base_damage + equipped_damage
    if attacker.autoact('dbledamg'):
        total_damage *= 2
    target.life -= total_damage
    target.save()
    return total_damage


def heal_self(character_is):
    diff = character_is.life_max - character_is.life
    character_is.life = character_is.life_max
    character_is.save()
    return diff