from django import template
from django.core.cache import cache
from django.conf import settings

from core.models import Team

register = template.Library()


@register.filter
def conference_teams(teams, conference):
    conference_teams = teams.filter(conference=conference)
    return conference_teams

# TODO this needs to move to a classmethod on team
@register.filter
def division_teams(teams, division):
    division_teams = Team.get_conference_division_teams(teams, division)
    return division_teams


# TODO this needs to move to a classmethod on team
# @register.filter
# def conference_stats(stats, conference):
#     key = 'conference-teams-{}'.format(conference)
#     conference_stats = cache.get(key)
#     if not conference_stats:
#         conference_stats = stats.filter(team__conference=conference)
#         cache.set(key, conference_stats, timeout=settings.TEAM_STATS_TIMEOUT)
#     return conference_stats


@register.filter
def rushing_attempts_leader(stats):
    return stats.order_by('-attempts').first()


@register.filter
def rushing_yards_leader(stats):
    return stats.order_by('-yards').first()


@register.filter
def rushing_touchdowns_leader(stats):
    return stats.order_by('-touchdowns').first()


@register.filter
def rushing_1st_leader(stats):
    return stats.order_by('-first_down').first()
