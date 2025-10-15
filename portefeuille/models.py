from django.db import models

class Actif(models.Model):
    nom = models.CharField(max_length=50)

class ETF(models.Model):
    nom = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10, unique=True)
