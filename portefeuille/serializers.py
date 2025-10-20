from rest_framework import serializers
#définit le formulaire que l'api accepte via un POST 

class SharpeInputSerializer(serializers.Serializer):
    #les champs envoyés par le user via l'api
    montant_initial_investissement = serializers.DecimalField(max_digits=20, decimal_places=2)
    montant_contribution_recurrente = serializers.DecimalField(max_digits=20, decimal_places=2)
    frequence_contribution = serializers.ChoiceField(choices=[1,2,3])
    duree_investissement = serializers.IntegerField()
    frais_gestion_annuels = serializers.DecimalField(max_digits=5, decimal_places=2)

    actifs = serializers.ListField(
        child = serializers.CharField(max_length=50), required=False,
        help_text = "Liste des types d'actifs : ACTIONS, OBLIGATIONS, ETF"
    )
    etfs_populaires = serializers.ListField(
        child = serializers.CharField(max_length=50), required=False,
        help_text = "Liste des ETF populaires sélectionnés"
    )

    expected_return = serializers.FloatField(required=False)
    volatility = serializers.FloatField(required=False)
    rendements = serializers.ListField(
        child = serializers.FloatField(),
        help_text ="Liste des rendements historiques (mensuels, journaliers, ...)"
    )
    risk_free_rate = serializers.FloatField(default=0.01)
