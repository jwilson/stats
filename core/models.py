from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils import timezone


ITEM_DEF = (
    ('0', 'EMPTY'),
    ('1', 'HEALTH'),
    ('2', 'WEALTH'),
    ('3', 'ENERGY'),
    ('4', 'WEAPON'),
    ('5', 'ARMOR'),
    ('6', 'ACCESSORY'),
    ('7', 'BUFF'),
    ('8', 'ACTION'),
)


WEAPON_DEF = (
    ('0', 'EMPTY'),
    ('1', 'ONE HAND DAGGER'),
    ('2', 'ONE HAND MACE'),
    ('3', 'ONE HAND PISTOL'),
    ('4', 'ONE HAND SPEAR'),
    ('5', 'ONE HAND SWORD'),
    ('6', 'TWO HAND AXE'),
    ('7', 'TWO HAND BOW'),
    ('8', 'TWO HAND CROSSBOW'),
    ('9', 'TWO HAND SHOOTING'),
    ('10', 'TWO HAND SPEAR'),
    ('11', 'TWO HAND STAFF'),
    ('12', 'TWO HAND SWORD'),
    ('13', 'ITEM'),
    ('14', 'SHIELD'),
    ('15', 'UNARMED'),
)

ARMOR_DEF = (
    ('0', 'EMPTY'),
    ('1', 'HEAD'),
    ('2', 'SHOULDERS'),
    ('3', 'CHEST'),
    ('4', 'WRISTS'),
    ('5', 'PANTS'),
    ('6', 'GLOVES'),
    ('7', 'WAIST'),
    ('8', 'BOOTS'),
)

ACCESSORY_DEF = (
    ('0', 'EMPTY'),
    ('1', 'RING'),
    ('2', 'AMULET'),
    ('3', 'TRINKET'),
)



# class Element(models.Model):
#     name = models.CharField(max_length=255, help_text="The name of the element")
#     icon = models.ImageField(upload_to='elements/')


# class Stat(models.Model):
#     name = models.CharField(max_length=255, help_text="The name of the stat")


# class ElementalStat(models.Model):
#     element = models.ForeignKey(Element, related_name='elemental_stats', help_text="The element of the state", on_delete=models.CASCADE)
#     stat = models.ForeignKey(Stat, related_name='elemental_stats', help_text="The element of the state", on_delete=models.CASCADE)


class PrefabPathMixin(object):
    def get_prefab_path(self):
        _model = self.__class__.__name__.lower()
        path = self.image.name.split('.')[0]
        synty_path = path[len(_model) + 1:]
        full_path = '{}.prefab'
        return full_path.format('/'.join(synty_path.split('-')))


class SaveMixin(object):
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        self.prefab_path = self.get_prefab_path()
        return super().save(*args, **kwargs)
        

class StatsObject(models.Model):
    level = models.PositiveIntegerField(default=1)
    health = models.FloatField(default=0)
    energy = models.FloatField(default=0)
    stamina = models.FloatField(default=0)
    intellect = models.FloatField(default=0)
    endurance = models.FloatField(default=0)
    resistance = models.FloatField(default=0)
    red_resistance = models.FloatField(default=0)
    blue_resistance = models.FloatField(default=0)
    green_resistance = models.FloatField(default=0)
    white_resistance = models.FloatField(default=0)
    black_resistance = models.FloatField(default=0)
    damage = models.FloatField(default=0)
    red_damage = models.FloatField(default=0)
    blue_damage = models.FloatField(default=0)
    green_damage = models.FloatField(default=0)
    white_damage = models.FloatField(default=0)
    black_damage = models.FloatField(default=0)
    durability = models.FloatField(default=0)
    weight = models.FloatField(default=0)

    class Meta:
        abstract = True


class Armor(PrefabPathMixin, SaveMixin, StatsObject):
    COUNT_CACHE_KEY = 'armors_count'
    name = models.CharField(max_length=255, help_text="The name of the armour")
    kind = models.CharField(max_length=255, choices=ARMOR_DEF)
    image = models.ImageField(upload_to='armor/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True)
    prefab_path = models.CharField(max_length=255)


@receiver(post_save, sender=Armor, dispatch_uid='update_weapons_count_cache')
def update_armors_count_cache(sender, instance, **kwargs):
    armors_count = sender.objects.all().count()
    cache.set(sender.COUNT_CACHE_KEY, armors_count, timeout=None)


class Weapon(PrefabPathMixin, SaveMixin, StatsObject):
    COUNT_CACHE_KEY = 'weapons_count'
    name = models.CharField(max_length=255, help_text="The name of the weapon")
    kind = models.CharField(max_length=255, choices=WEAPON_DEF)
    image = models.ImageField(upload_to='weapon/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True)
    prefab_path = models.CharField(max_length=255)


@receiver(post_save, sender=Weapon, dispatch_uid='update_weapons_count_cache')
def update_weapons_count_cache(sender, instance, **kwargs):
    weapons_count = sender.objects.all().count()
    cache.set(sender.COUNT_CACHE_KEY, weapons_count, timeout=None)



# class Character(models.Model):
#     name = models.CharField(max_length=255, help_text="The name of the character")


# class Spell(models.Model):
#     name = models.CharField(max_length=255, help_text="The name of the spell")
#     icon = models.ImageField(upload_to='spells/')
#     min_level = models.PositiveIntegerField()


# class Item(models.Model):
#     name = models.CharField(max_length=255, help_text="The name of the item")
#     icon = models.ImageField(upload_to='items/')
#     min_level = models.PositiveIntegerField()


# class Enemy(models.Model):
#     name = models.CharField(max_length=255, help_text="The name of the enemy")


# class State(models.Model):
#     name = models.CharField(max_length=255, help_text="The name of the state")



# UNUSED FOR NOW


# class Ability(models.Model):
#     pass


# class Quest(models.Model):
#     pass


# class Location(models.Model):
#     pass
