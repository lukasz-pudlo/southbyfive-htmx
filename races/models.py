from django.db import models


class Race(models.Model):
    PARK_CHOICES = {
        "KP": "King's Park",
        "LP": "Linn Park",
        "RG": "Rouken Glen",
        "PP": "Pollock Park",
        "BP": "Bellahouston Park",
        "QP": "Queen's Park",
    }
    park = models.CharField(
        max_length=2,
        choices=PARK_CHOICES,
    )
    season = models.CharField(
        max_length=9,
    )


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


class Result(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE)
    position = models.IntegerField()
    time = models.DurationField(null=True)
