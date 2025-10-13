from django.db import models
from django.utils.text import slugify


class Season(models.Model):
    # 2526 for 2025/2026
    season = models.CharField(
        max_length=4, unique=True, help_text="For 2025/2026 season, enter 2526")

    def __str__(self):
        first_part = self.season[:2]
        second_part = self.season[2:]
        return f"{first_part}/{second_part}"


class Race(models.Model):
    PARK_CHOICES = {
        "KP": "King's Park",
        "LP": "Linn Park",
        "RG": "Rouken Glen",
        "PP": "Pollok Park",
        "BP": "Bellahouston Park",
        "QP": "Queen's Park",
    }
    park = models.CharField(
        max_length=2,
        choices=PARK_CHOICES,
    )
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.get_park_display()

    def save(self, *args, **kwargs):
        self.slug = f"{self.park.lower()}-{self.season.season}"
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['park', 'season']


class Runner(models.Model):
    full_name = models.CharField(
        max_length=256,
    )
    GENDER_CHOICES = {
        "M": "Male",
        "F": "Female",
        "NB": "Non-Binary",
    }
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
    )

    def __str__(self):
        return self.full_name


class Result(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE)
    position = models.IntegerField()
    time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.runner} - {str(self.time) if {self.time} else 'No time'}"
