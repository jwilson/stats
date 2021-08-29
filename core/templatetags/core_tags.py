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

