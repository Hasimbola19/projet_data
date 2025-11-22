from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SimulerPortefeuilleSerializer
from .func import (
    telecharger_donnees_marche, calculer_rendements, calculer_sharpe_ratio,
    calculer_volatilite, calculer_rendement_moyen, calculer_cagr,
    simuler_investissement_dca, predire_regression_lineaire
)
import numpy as np

class SimuerPortefeuilleView(APIView):
    def post(self, request):
        serializer = SimulerPortefeuilleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data

        # --- Paramètres ---
        montant_initial = float(data['montant_initial'])
        montant_contribution = float(data['montant_contribution'])
        frequence = data['frequence_contribution']
        duree = data['duree_investissement']
        frais = float(data['frais_gestion_annuels'])
        actifs = data['actifs']
        risques = data['risques']
        periode = data['periode_historique']

        rendements_portefeuille = None
        composition = []

        # --- Calcul des rendements du portefeuille ---
        for actif in actifs:
            ticker = actif['ticker']
            ponderation = float(actif['ponderation']) / 100

            df = telecharger_donnees_marche(ticker, periode)
            if df.empty:
                return Response({"error": f"Impossible de télécharger {ticker}"}, status=status.HTTP_400_BAD_REQUEST)
            
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

        rendements_array = np.array(rendements_portefeuille.values, dtype=float)

        rendement_moyen = calculer_rendement_moyen(rendements_array)
        volatilite = calculer_volatilite(rendements_array)
        sharpe = calculer_sharpe_ratio(rendements_array, risques)

        # --- Simulation portefeuille DCA ---
        simulation_dca = simuler_investissement_dca(
            montant_initial, montant_contribution, frequence, duree, rendement_moyen, frais
        )

        cagr = calculer_cagr(montant_initial, simulation_dca['valeur_finale'], duree)

        # --- ACWI simulé et aligné sur le portefeuille ---
        acwi_df = telecharger_donnees_marche("ACWI", periode)
        acwi_data = []
        if not acwi_df.empty:
            acwi_rendements = calculer_rendements(acwi_df['Close'])
            acwi_simulation = simuler_investissement_dca(
                montant_initial,
                montant_contribution,
                frequence,
                duree,
                calculer_rendement_moyen(acwi_rendements.values),
                frais
            )
            annees_portefeuille = [d['annee'] for d in simulation_dca['donnees_annuelles']]
            acwi_dict = {d['annee']: d['valeur'] for d in acwi_simulation['donnees_annuelles']}
            acwi_data = [
                {'annee': annee, 'valeur': round(acwi_dict.get(annee, list(acwi_dict.values())[-1]), 2)}
                for annee in annees_portefeuille
            ]

        # --- Fréquences lisibles ---
        frequences_map = {1: "Mensuel", 2: "Trimestriel", 4: "Semestriel", 12: "Annuel"}

        # --- Réponse ---
        return Response({
            'parametres': {
                'montant_initial': montant_initial,
                'contribution': montant_contribution,
                'frequence': frequences_map.get(frequence, frequence),
                'duree': duree,
                'frais': frais,
                'actifs': [{"ticker": actif['ticker']}]
            },
            'ratios_financiers': {
                'rendement_moyen_annuel': round(rendement_moyen * 100, 2),
                'volatilite_annuelle': round(volatilite * 100, 2),
                'sharpe_ratio': round(sharpe, 3),
                'cagr': round(cagr * 100, 2),
                'rendement_total': simulation_dca['rendement_total']
            },
            'simulation': simulation_dca,
            'acwi': acwi_data
        })
