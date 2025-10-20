from django import template

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
