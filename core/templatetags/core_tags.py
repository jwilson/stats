from django import template

register = template.Library()


@register.filter
def conference_teams(teams, conference):
    conference_teams = teams.filter(conference=conference)
    return conference_teams


@register.filter
def division_teams(teams, division):
    division_teams = teams.filter(division=division)
    return division_teams


@register.filter
def conference_stats(stats, conference):
    conference_stats = stats.filter(team__conference=conference)
    return conference_stats


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
