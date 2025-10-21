from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


class Season(models.Model):
    # 2526 for 2025/2026
    season = models.CharField(
        max_length=4,
        unique=True,
        help_text="For 2025/2026 season, enter 2526"
    )

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
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    GENDER_CHOICES = {
        "M": "Male",
        "F": "Female",
        "NB": "Non-Binary",
    }
    CATEGORY_CHOICES = {
        "MS": "Male Senior",
        "FS": "Female Senior",
        "NBS": "Non-Binary Senior",
        "M40": "Male 40",
        "F40": "Female 40",
        "NB40": "Non-Binary 40",
        "M50": "Male 50",
        "F50": "Female 50",
        "NB50": "Non-Binary 50",
        "M60": "Male 60",
        "F60": "Female 60",
        "NB60": "Non-Binary 60",
        "M70": "Male 70",
        "F70": "Female 70",
        "NB70": "Non-Binary 70",
        "M80": "Male 80",
        "F80": "Female 80",
        "NB80": "Non-Binary 80",
        "M90": "Male 90",
        "F90": "Female 90",
        "NB90": "Non-Binary 90",
        "M100": "Male 100",
        "F100": "Female 100",
        "NB100": "Non-Binary 100",
    }
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
    )
    participant_number = models.CharField(max_length=5)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    club = models.CharField(max_length=256, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Result(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE)
    time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.runner} - {str(self.time) if {self.time} else 'No time'}"


class RecalculatedResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE)
    time = models.DurationField(null=True, blank=True)
    points = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.runner} - {str(self.time) if {self.time} else 'No time'}"


class Classification(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = f"class-{self.race.park.lower()}-{self.season.season}"
        super().save(*args, **kwargs)


class ClassificationResult(models.Model):
    classification = models.ForeignKey(
        Classification, on_delete=models.CASCADE)
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE)
    general_points = models.IntegerField(null=True)
    gender_points = models.IntegerField(null=True)
    category_points = models.IntegerField(null=True)


class RaceFile(models.Model):
    excel_file = models.FileField(null=True, blank=True, validators=[
        FileExtensionValidator(['xlsx'])])
