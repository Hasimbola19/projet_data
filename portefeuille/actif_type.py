from .models import Actif
# créer les types d'actifs
def creer_actifs_de_base():
    for nom in ["ETF", "ACTION", "OBLIGATIONS"]:
        Actif.objects.get_or_create(nom=nom)
