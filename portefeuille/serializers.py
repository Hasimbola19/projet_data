from rest_framework import serializers
from datetime import datetime


class SimulerPortefeuilleSerializer(serializers.Serializer):
    # Types de données recu de la part de serveur client
    annee_debut = serializers.IntegerField(required=False, min_value=1900, max_value=2100)
    annee_fin = serializers.IntegerField(required=False, min_value=1900, max_value=2100)
    montant_initial = serializers.DecimalField(max_digits=15, decimal_places=2)
    montant_contribution = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)
    frequence_contribution = serializers.ChoiceField(choices=[1, 4, 2, 12], default=1)
    duree_investissement = serializers.IntegerField(min_value=1)
    frais_gestion_annuels = serializers.DecimalField(max_digits=5, decimal_places=2, default=0.2)
    
    # Composition du portefeuille
    actifs = serializers.ListField(
        child=serializers.DictField(),
        help_text="Liste de {ticker, ponderation}"
    )
    
    risques = serializers.FloatField(default=0.02)
    periode_historique = serializers.CharField(default="5y")
    taux_inflation = serializers.FloatField(default=0.02, help_text="Taux d'inflation annuel (ex: 0.02 pour 2%)")
    
    def validate(self, data):
        """Convertir les années en dates complètes"""
        if 'annee_debut' in data and data['annee_debut']:
            # Créer une date au 1er janvier de l'année
            data['date_debut'] = datetime(data['annee_debut'], 1, 1)
        
        if 'annee_fin' in data and data['annee_fin']:
            # Créer une date au 31 décembre de l'année
            data['date_fin'] = datetime(data['annee_fin'], 12, 31)
        
        return data
