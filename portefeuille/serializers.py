from rest_framework import serializers


class SimulerPortefeuilleSerializer(serializers.Serializer):
    # Types de données recu de la part de serveur client
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
