from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SimulerPortefeuilleSerializer
from .func import (
    telecharger_donnees_marche, calculer_rendements, calculer_sharpe_ratio,
    calculer_volatilite, calculer_rendement_moyen, calculer_cagr,
    simuler_investissement_dca
)

# View pour les calculs et le renvoi des données 
class SimuerPortefeuilleView(APIView):
    # Requête de type post pour récupérer les données de la requête client et faire le calcul
    def post(self, request):
        serializer = SimulerPortefeuilleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer les données depuis la cors de la requete du clien
        data = serializer.validated_data

        # Récupérer les Paramètres
        montant_initial = float(data['montant_initial'])
        montant_contribution = float(data['montant_contribution'])
        frequence = data['frequence_contribution']
        duree = data['duree_investissement']
        frais = float(data['frais_gestion_annuels'])
        actifs = data['actifs']
        risques = data['risques']
        periode = data['periode_historique']

        # Télécharger les données de chaque actif
        rendements_portefeuille = None
        composition = []

        for actif in actifs:
            ticker = actif['ticker']
            ponderation = float(actif['ponderation']) / 100

            # Tél"charger les données depuis yfinance
            df = telecharger_donnees_marche(ticker, periode)
            if df.empty:
                return Response(
                    {"error": f"impossible de tékécharger {ticker}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Caclculer les rendements
            rendements = calculer_rendements(df['Close'])
            if rendements_portefeuille is None:
                rendements_portefeuille = rendements * ponderation
            else:
                rendements_portefeuille = rendements_portefeuille.add(rendements * ponderation, fill_value=0)
            
            composition.append({
                'ticker': ticker,
                'ponderation': actif['ponderation'],
                'rendement_moyen': round(calculer_rendement_moyen(rendements.values) * 100, 2),
                'volatilite': round(calculer_volatilite(rendements.values) * 100, 2)
            })
        
        # Calculer les ratios
        rendements_array = rendements_portefeuille.values
        rendement_moyen = calculer_rendement_moyen(rendements_array)
        volatilite = calculer_volatilite(rendements_array)
        sharpe = calculer_sharpe_ratio(rendements_array, risques)

        # Simuler DCA
        simulation_dca = simuler_investissement_dca(
            montant_initial, montant_contribution, frequence, duree, rendement_moyen, frais
        )

        cagr = calculer_cagr(montant_initial, simulation_dca['valeur_finale'], duree)

        return Response({
            'parametres': {
                'montant_initial': montant_initial,
                'contribution': montant_contribution,
                'frequence': ['Mensuel', 'Trimestriel', 'Semestriel', 'Annuel'][
                    [1, 4, 2, 12].index(frequence)
                ],
                'duree': duree,
                'frais': float(data['frais_gestion_annuels'])
            },
            'composition': composition,
            'ratios_financiers': {
                'rendement_moyen_annuel': round(rendement_moyen * 100, 2),
                'volatilite_annuelle': round(volatilite * 100, 2),
                'sharpe_ratio': round(sharpe, 3),
                'cagr': round(cagr * 100, 2),
                'rendement_total': simulation_dca['rendement_total']
            },
            'simulation': simulation_dca
        })
