from .models import Actif

def creer_actifs_de_base():
    for nom in ["ETF", "ACTION", "OBLIGATIONS"]:
        Actif.objects.get_or_create(nom=nom)