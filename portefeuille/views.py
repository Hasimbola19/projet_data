from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SimulerPortefeuilleSerializer
from .func import (
    telecharger_donnees_marche, calculer_rendements, calculer_sharpe_ratio,
    calculer_volatilite, calculer_rendement_moyen, calculer_cagr,
    simuler_investissement_dca, simuler_investissement_dca_historique, predire_regression_lineaire,
    calculer_rendements_periode, calculer_impact_inflation, comparer_avec_indice, predire_avec_volatilite,
    calculer_histogramme_rendements, simuler_lump_sum
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
        date_debut = data.get('date_debut')
        date_fin = data.get('date_fin')

        rendements_portefeuille = None
        prix_portefeuille = None
        composition = []

        # --- Calcul des rendements du portefeuille ---
        for actif in actifs:
            ticker = actif['ticker']
            ponderation = float(actif['ponderation']) / 100

            df = telecharger_donnees_marche(ticker, periode, date_debut, date_fin)
            if df.empty:
                return Response(
                    {"error": f"impossible de télécharger {ticker}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculer les rendements en utilisant la valeur High (prix max journalier)
            rendements = calculer_rendements(df['High'])
            if rendements_portefeuille is None:
                rendements_portefeuille = rendements * ponderation
                # Construire les prix du portefeuille pondéré
                prix_portefeuille = df['High'] * ponderation
                date_derniere = df.index[-1]
            else:
                rendements_portefeuille = rendements_portefeuille.add(rendements * ponderation, fill_value=0)
                # Ajouter au prix du portefeuille
                prix_portefeuille = prix_portefeuille.add(df['High'] * ponderation, fill_value=0)
            
            composition.append({
                'ticker': ticker,
                'ponderation': actif['ponderation'],
                'rendement_moyen': round(calculer_rendement_moyen(rendements.values) * 100, 2),
                'volatilite': round(calculer_volatilite(rendements.values) * 100, 2),
            })

        rendements_array = np.array(rendements_portefeuille.values, dtype=float)

        rendement_moyen = calculer_rendement_moyen(rendements_array)
        volatilite = calculer_volatilite(rendements_array)
        # Utiliser l'Euribor 3 mois comme taux sans risque
        sharpe = calculer_sharpe_ratio(rendements_array)

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
        # Alternatives possibles : ACWI
        comparaison_indice = None
        try:
            # Essayer différents tickers pour l'indice mondial
            tickers_indices = ['ACWI']
            df_indice = None
            ticker_utilise = None
            
            for ticker_indice in tickers_indices:
                df_indice = telecharger_donnees_marche(ticker_indice, periode, date_debut, date_fin)
                if not df_indice.empty and len(df_indice) > 10:  # Au moins 10 jours de données
                    ticker_utilise = ticker_indice
                    break
            
            if df_indice is not None and not df_indice.empty:
                # Aligner les dates avec le portefeuille
                prix_indice = df_indice['High'].reindex(prix_portefeuille.index, method='ffill')
                # Vérifier qu'il y a des données valides
                if not prix_indice.isna().all():
                    comparaison_indice = comparer_avec_indice(
                        montant_initial, montant_contribution, frequence, 
                        prix_portefeuille, prix_indice, frais
                    )
                    # Ajouter le nom du ticker utilisé
                    if comparaison_indice:
                        comparaison_indice['indice']['nom'] = f'Indice Mondial ({ticker_utilise})'
        except Exception as e:
            # Si la comparaison échoue, continuer sans
            print(f"Erreur comparaison indice: {e}")
            pass

        # Prédiction avec régression linéaire et bandes de volatilité
        predictions_futures = []
        if len(donnees_annuelles) > 1:
            # Préparer les données pour la régression
            X = np.array([[d['annee']] for d in donnees_annuelles])
            y = np.array([d['valeur'] for d in donnees_annuelles])
            
            # Prédire les 5 prochaines années avec bandes de volatilité (journalièrement)
            date_debut_sim = prix_portefeuille.index[0]
            date_fin_sim = prix_portefeuille.index[-1]
            predictions_futures, sigma = predire_avec_volatilite(X, y, date_debut_sim, date_fin_sim, nb_annees_futures=5)

        # Calculer l'histogramme des rendements mensuels
        histogramme_rendements = calculer_histogramme_rendements(simulation_dca['donnees_mensuelles'])
        
        # Simuler Lump Sum pour comparaison
        simulation_lump_sum = simuler_lump_sum(montant_initial, prix_portefeuille, frais)

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
                'actifs': [{"ticker": actif['ticker'], "ponderation": actif['ponderation']} for actif in actifs]
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
            'predictions_futures': predictions_futures,
            'histogramme_rendements': histogramme_rendements,
            'simulation_lump_sum': simulation_lump_sum
        })
