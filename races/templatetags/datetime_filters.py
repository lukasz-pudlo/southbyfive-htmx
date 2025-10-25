from django import template
from datetime import datetime

register = template.Library()


@register.filter
def format_race_time(value):
    """
    Format a timedelta object as HH:MM:SS
    """
    if value is None:
        return "DNF"

    total_seconds = int(value.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


@register.filter
def format_season_name(value):
    """
    Format season as YYYY/YYYY
    """
    first_year_str = str(value[:2])
    second_year_str = str(value[2:])
    first_dt = datetime.strptime(first_year_str, '%y')
    second_dt = datetime.strptime(second_year_str, '%y')
    return f"{first_dt.strftime('%Y')}/{second_dt.strftime('%Y')}"
