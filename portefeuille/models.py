# contient les modeles de bdd
from django.db import models

#type d'actif
class Actif(models.Model):
    nom = models.CharField(max_length=50)
#etf avec un nom et un code unique ole ticker
class ETF(models.Model):
    nom = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10, unique=True)
