DJGE
====

### TODO
* Add world.models.Location.get_npcs('attitude') to return any NPCs that spawn at that location matching given attitude

* Make it possible to link multiple mobile.categories to a single world.location so we can spawn
 multiple types of combatants during random encounters.


* Equips need to go back into BaseMobile, NPCs can equip stuff too
* Charecter/equip weapon, dropdown, queryset=Items.obj.filter(character).filter(offense)

* pacifist system, value in battle model, code in battlestack
* kill type count belongs to account, store it in player.models.Config, use throughs
* rename 'playing_toon' to 'playing_character'
* I can probably replace "Combatant" with "NPC" because most (if not all) of the methods would apply to nonhostiles
