from django.db import models


class Season(models.Model):
    season_start_year = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.season_start_year}/{int(self.season_start_year)+1}"


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
    season = models.CharField(
        max_length=9,
    def __str__(self):
        return self.get_park_display()

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
