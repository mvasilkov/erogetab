from django.db import models

class Game(models.Model):
    dlsite = models.CharField(blank=True, max_length=6)
    dlsite_has_eng = models.BooleanField()
    dlsite_name = models.CharField(max_length=250)
    dlsite_name_eng = models.CharField(blank=True, max_length=250)

    def __str__(self):
        return 'RJ' + self.dlsite
