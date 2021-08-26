from django.core.cache import cache

# from core.models import Armor, Weapon


# def item_counts(request):
#     armors_count = cache.get(Armor.COUNT_CACHE_KEY)
#     if not armors_count:
#         armors_count = Armor.objects.all().count()
#         cache.set(Armor.COUNT_CACHE_KEY, armors_count, timeout=None)
#     weapons_count = cache.get(Weapon.COUNT_CACHE_KEY)
#     if not weapons_count:
#         weapons_count = Weapon.objects.all().count()
#         cache.set(Weapon.COUNT_CACHE_KEY, weapons_count, timeout=None)
#     return {'weapons_count': weapons_count, 'armors_count': armors_count}
