from django.db import models

class Game(models.Model):
    dlsite = models.CharField(blank=True, max_length=6)
    dlsite_has_eng = models.BooleanField()
    dlsite_name = models.CharField(blank=True, max_length=250)
    dlsite_name_eng = models.CharField(blank=True, max_length=250)

    getchu = models.CharField(blank=True, max_length=6)
    getchu_name = models.CharField(blank=True, max_length=250)

    def __str__(self):
        if self.dlsite:
            return 'RJ' + self.dlsite
        elif self.getchu:
            return 'CHU' + self.getchu
        return 'BAD GAME'

class OverrideFilename(models.Model):
    name = models.CharField(max_length=250)
    filename = models.CharField(max_length=250)
