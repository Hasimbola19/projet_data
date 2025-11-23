from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SimulerPortefeuilleSerializer
from .func import (
    telecharger_donnees_marche, calculer_rendements, calculer_sharpe_ratio,
    calculer_volatilite, calculer_rendement_moyen, calculer_cagr,
    simuler_investissement_dca, simuler_investissement_dca_historique, predire_regression_lineaire,
    calculer_rendements_periode, calculer_impact_inflation, comparer_avec_indice
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
        prix_portefeuille = None
        composition = []

        # --- Calcul des rendements du portefeuille ---
        for actif in actifs:
            ticker = actif['ticker']
            ponderation = float(actif['ponderation']) / 100

            df = telecharger_donnees_marche(ticker, periode)
            if df.empty:
                return Response(
                    {"error": f"impossible de télécharger {ticker}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculer les rendements 
            rendements = calculer_rendements(df['Close'])
            if rendements_portefeuille is None:
                rendements_portefeuille = rendements * ponderation
                # Construire les prix du portefeuille pondéré
                prix_portefeuille = df['Close'] * ponderation
                date_derniere = df.index[-1]
            else:
                rendements_portefeuille = rendements_portefeuille.add(rendements * ponderation, fill_value=0)
                # Ajouter au prix du portefeuille
                prix_portefeuille = prix_portefeuille.add(df['Close'] * ponderation, fill_value=0)
            
            composition.append({
                'ticker': ticker,
                'ponderation': actif['ponderation'],
                'rendement_moyen': round(calculer_rendement_moyen(rendements.values) * 100, 2),
                'volatilite': round(calculer_volatilite(rendements.values) * 100, 2),
            })

        rendements_array = np.array(rendements_portefeuille.values, dtype=float)

        rendement_moyen = calculer_rendement_moyen(rendements_array)
        volatilite = calculer_volatilite(rendements_array)
        sharpe = calculer_sharpe_ratio(rendements_array, risques)

        # Simuler DCA avec les prix historiques réels
        simulation_dca = simuler_investissement_dca_historique(
            montant_initial, montant_contribution, frequence, prix_portefeuille, frais
        )

        # Calculer les rendements périodiques détaillés
        donnees_annuelles = simulation_dca['donnees_annuelles']
        rendements_detailles = calculer_rendements_periode(donnees_annuelles)
        
        # Calculer l'impact de l'inflation
        duree_reelle = (prix_portefeuille.index[-1] - prix_portefeuille.index[0]).days / 365.25
        impact_inflation = calculer_impact_inflation(
            simulation_dca['valeur_finale'],
            simulation_dca['montant_investi'],
            duree_reelle,
            data.get('taux_inflation', 0.02)
        )

        # Comparaison avec l'indice ACWI IMI
        # Ticker pour ACWI IMI : ACWI (MSCI All Country World Index)
        comparaison_indice = None
        try:
            df_indice = telecharger_donnees_marche('ACWI', periode)
            if not df_indice.empty:
                # Aligner les dates avec le portefeuille
                prix_indice = df_indice['Close'].reindex(prix_portefeuille.index, method='ffill')
                comparaison_indice = comparer_avec_indice(
                    montant_initial, montant_contribution, frequence, 
                    prix_portefeuille, prix_indice, frais
                )
        except Exception as e:
            # Si la comparaison échoue, continuer sans
            pass

        # Prédiction avec régression linéaire
        if len(donnees_annuelles) > 1:
            # Préparer les données pour la régression
            X = np.array([[d['annee']] for d in donnees_annuelles])
            y = np.array([d['valeur'] for d in donnees_annuelles])
            
            # Prédire les 3-5 prochaines années
            annees_futures = 3
            X_pred = np.array([[duree + i] for i in range(1, annees_futures + 1)])
            predictions = predire_regression_lineaire(X, y, X_pred)
            
            predictions_futures = [
                {
                    'annee': int(duree + i + 1),
                    'valeur_predite': round(float(predictions[i]), 2)
                }
                for i in range(len(predictions))
            ]

        # --- Fréquences lisibles ---
        frequences_map = {1: "Mensuel", 2: "Trimestriel", 4: "Semestriel", 12: "Annuel"}

        # --- Réponse ---
        return Response({
            'parametres': {
                'date_debut': prix_portefeuille.index[0].strftime('%Y-%m-%d'),
                'date_fin': prix_portefeuille.index[-1].strftime('%Y-%m-%d'),
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
                'cagr': simulation_dca['cagr'],
                'rendement_total': simulation_dca['rendement_total']
            },
            'simulation': simulation_dca,
            'rendements_detailles': rendements_detailles,
            'impact_inflation': impact_inflation,
            'comparaison_indice': comparaison_indice,
            'predictions_futures': predictions_futures
        })
