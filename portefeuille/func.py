import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import math

def nettoyer_valeur(valeur):
    """Convertit les valeurs NaN, inf en None ou en valeur valide pour JSON"""
    if valeur is None:
        return None
    if isinstance(valeur, (np.floating, float)):
        if math.isnan(valeur) or math.isinf(valeur):
            return None
    return valeur

def nettoyer_donnees(donnees):
    """Nettoie récursivement un dict ou une liste de valeurs NaN/inf"""
    if isinstance(donnees, dict):
        return {cle: nettoyer_donnees(valeur) for cle, valeur in donnees.items()}
    elif isinstance(donnees, list):
        return [nettoyer_donnees(item) for item in donnees]
    else:
        return nettoyer_valeur(donnees)

'''  telecharger_donnees_marche(ticker, periode="5y")
    calculer_rendements(prix)
    calculer_volatilite(rendements, annualiser=True)
    calculer_rendement_moyen(rendements, annualiser=True)
    calculer_sharpe_ratio(rendements, risk_free_rate=0.02) // on a besoin de rendement et de volatilité
    calculer_cagr(valeur_initiale, valeur_finale, nb_annees)
    simuler_investissement_dca(montant_initial, contribution, frequence, duree_annees, rendement_annuel, frais_annuels=0)
    predire_regression_lineaire(X, y, X_pred)
'''
def telecharger_donnees_marche(ticker, periode="5y", date_debut=None, date_fin=None):
    #Téléchargement des données historiques depuis Yahoo Finance
    try:
        etf = yf.Ticker(ticker)
        
        # Si des dates spécifiques sont fournies, les utiliser
        if date_debut and date_fin:
            # Convertir en string format YYYY-MM-DD si nécessaire
            if hasattr(date_debut, 'strftime'):
                date_debut = date_debut.strftime('%Y-%m-%d')
            if hasattr(date_fin, 'strftime'):
                date_fin = date_fin.strftime('%Y-%m-%d')
            return etf.history(start=date_debut, end=date_fin)
        else:
            return etf.history(period=periode)
    except:
        return pd.DataFrame()
    
def calculer_rendements(prix):
    #Calcule les rendements quotidiens à partir des prix de clôture ajustés
    return prix.pct_change().dropna()  

def calculer_volatilite(rendements, annualiser=True):
    #Calcule la volatilité des rendements
    volatilite = rendements.std()
    if annualiser:
        volatilite *= (252 ** 0.5)  
    return volatilite

def calculer_rendement_moyen(rendements, annualiser=True):
    #Calcule le rendement moyen 
    rendement_moyen = rendements.mean()
    if annualiser:
        rendement_moyen *= 252  # Annualisation pour les rendements quotidiens
    return rendement_moyen          

def obtenir_euribor_3m():
    """Télécharge le taux Euribor 3 mois actuel depuis Yahoo Finance"""
    try:
        # Télécharger l'Euribor 3 mois (ticker: EURIBOR3MD=X ou utiliser un proxy)
        euribor = yf.Ticker("^IRX")  # T-Bill 13 semaines comme proxy
        hist = euribor.history(period="5d")
        if not hist.empty:
            # Retourner le dernier taux disponible (en pourcentage, diviser par 100)
            return hist['Close'].iloc[-1] / 100
    except:
        pass
    
    # Valeur par défaut si échec (Euribor 3m moyen historique ~3%)
    return 0.03

def calculer_sharpe_ratio(rendements, risk_free_rate=None): 
    #Calcule le ratio de Sharpe avec l'Euribor 3 mois comme taux sans risque
    if risk_free_rate is None:
        risk_free_rate = obtenir_euribor_3m()
    
    rendement_moyen = calculer_rendement_moyen(rendements)
    volatilite = calculer_volatilite(rendements)
    if volatilite == 0:
        return 0
    sharpe_ratio = (rendement_moyen - risk_free_rate) / volatilite
    return sharpe_ratio

def calculer_cagr(valeur_initiale, valeur_finale, nb_annees):
    #Calcule le taux de croissance annuel composé (CAGR)
    if valeur_initiale <= 0 or nb_annees <= 0:
        return 0
    cagr = (valeur_finale / valeur_initiale) ** (1 / nb_annees) - 1
    return cagr

def calculer_cagr_dca(montant_initial, contribution_mensuelle, valeur_finale, nb_annees):
    """
    Calcule le CAGR pour un investissement DCA
    Formule : ((Valeur_finale / Montant_total_investi) ^ (1 / nb_annees)) - 1
    """
    if nb_annees <= 0:
        return 0
    
    # Calcul du montant total investi (A)
    montant_total_investi = montant_initial + (contribution_mensuelle * 12 * nb_annees)
    
    if montant_total_investi <= 0:
        return 0
    
    # Formule CAGR : ((Vfinal / A) ^ (1 / t)) - 1
    cagr = (valeur_finale / montant_total_investi) ** (1 / nb_annees) - 1
    
    return cagr

def simuler_investissement_dca_historique(montant_initial, contribution, frequence, prix_historiques, frais_annuels=0):
    """
    Simule un investissement DCA en utilisant les prix historiques réels avec données journalières
    prix_historiques : pandas Series avec les prix et les dates en index
    """
    from dateutil.relativedelta import relativedelta
    from datetime import timedelta
    
    # Déterminer le nombre de périodes par an
    if frequence == 1:
        periode_par_an = 12
        delta_periode = relativedelta(months=1)
    elif frequence == 2:
        periode_par_an = 4
        delta_periode = relativedelta(months=3)
    elif frequence == 4:
        periode_par_an = 2
        delta_periode = relativedelta(months=6)
    else:
        periode_par_an = 1
        delta_periode = relativedelta(years=1)
    
    # Frais de gestion
    frais_annuels_decimal = frais_annuels / 100
    frais_par_jour = frais_annuels_decimal / 365
    frais_par_periode = frais_annuels_decimal / periode_par_an
    
    # Initialisation
    date_debut = prix_historiques.index[0].to_pydatetime()
    date_fin = prix_historiques.index[-1].to_pydatetime()
    
    valeur_portefeuille = 0
    parts_detenues = 0
    contribution_totale = 0
    donnees_annuelles = []
    donnees_journalieres = []
    
    date_contribution = date_debut
    periode = 0
    annee_actuelle = 0
    
    # Premier investissement
    prix_actuel = prix_historiques.iloc[0]
    parts_detenues = montant_initial / prix_actuel
    contribution_totale = montant_initial
    
    # Calculer la valeur du portefeuille pour chaque jour
    for date_actuelle in prix_historiques.index:
        date_py = date_actuelle.to_pydatetime()
        
        # Vérifier si c'est une date de contribution
        if date_py >= date_contribution and contribution > 0:
            prix_proche = prix_historiques.loc[date_actuelle]
            if not pd.isna(prix_proche):
                parts_achetees = contribution / prix_proche
                parts_detenues += parts_achetees
                contribution_totale += contribution
                # Prochaine contribution
                date_contribution = date_contribution + delta_periode
                periode += 1
        
        # Récupérer le prix du jour
        prix_jour = prix_historiques.loc[date_actuelle]
        if pd.isna(prix_jour):
            continue
        
        # Appliquer les frais de gestion journaliers
        parts_detenues = parts_detenues * (1 - frais_par_jour)
        
        # Calculer la valeur du portefeuille
        valeur_portefeuille = parts_detenues * prix_jour
        
        # Enregistrer les données journalières
        donnees_journalieres.append({
            'date': date_py.strftime('%Y-%m-%d'),
            'valeur': round(valeur_portefeuille, 2) if valeur_portefeuille is not None else 0,
            'contributions': round(contribution_totale, 2) if contribution_totale is not None else 0,
            'gain': round(valeur_portefeuille - contribution_totale, 2) if valeur_portefeuille is not None and contribution_totale is not None else 0
        })
        
        # Enregistrer les données annuelles
        if periode > 0 and periode % periode_par_an == 0:
            if annee_actuelle < periode // periode_par_an:
                annee_actuelle = periode // periode_par_an
                donnees_annuelles.append({
                    'annee': annee_actuelle,
                    'date': date_py.strftime('%Y-%m-%d'),
                    'valeur': round(valeur_portefeuille, 2) if valeur_portefeuille is not None else 0,
                    'contributions': round(contribution_totale, 2) if contribution_totale is not None else 0,
                    'gain': round(valeur_portefeuille - contribution_totale, 2) if valeur_portefeuille is not None and contribution_totale is not None else 0
                })
    
    # Calculer le CAGR réel
    duree_annees = (date_fin - date_debut).days / 365.25
    contribution_mensuelle = contribution if frequence == 1 else contribution * (12 / periode_par_an)
    cagr_dca = calculer_cagr_dca(montant_initial, contribution_mensuelle, valeur_portefeuille, duree_annees)
    
    resultat = {
        'valeur_finale': round(valeur_portefeuille, 2),
        'montant_investi': round(contribution_totale, 2),
        'gain_total': round(valeur_portefeuille - contribution_totale, 2),
        'rendement_total': round((valeur_portefeuille - contribution_totale) / contribution_totale * 100, 2) if contribution_totale > 0 else 0,
        'cagr': round(cagr_dca * 100, 2),
        'contribution_totale': round(contribution_totale, 2),
        'donnees_annuelles': donnees_annuelles,
        'donnees_mensuelles': donnees_journalieres
    }
    return nettoyer_donnees(resultat)

def simuler_investissement_dca(montant_initial, contribution, frequence, duree_annees, rendement_annuel, frais_annuels=0, date_debut=None):
    #Simule un investissement en DCA (Dollar-Cost Averaging) avec rendements moyens
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    # Si pas de date fournie, utiliser la date actuelle
    if date_debut is None:
        date_debut = datetime.now()
    elif hasattr(date_debut, 'to_pydatetime'):
        # Convertir Timestamp pandas en datetime
        date_debut = date_debut.to_pydatetime()
    
    # Déterminer le nombre de périodes par an en fonction de la fréquence
    if frequence == 1:
        periode_par_an = 12
        delta_periode = relativedelta(months=1)
    elif frequence == 2:
        periode_par_an = 4
        delta_periode = relativedelta(months=3)
    elif frequence == 4:
        periode_par_an = 2
        delta_periode = relativedelta(months=6)
    else:
        periode_par_an = 1
        delta_periode = relativedelta(years=1)

    nb_periodes = duree_annees * periode_par_an 
    rendement_periode = (1 + rendement_annuel) ** (1 / periode_par_an) - 1
    # Convertir les frais annuels en pourcentage (ex: 0.2 = 0.2%)
    frais_annuels_decimal = frais_annuels / 100
    frais_par_periode = frais_annuels_decimal / periode_par_an

    valeur_portefeuille = montant_initial
    contribution_totale = 0
    donnees_annuelles = []
    date_actuelle = date_debut
    
    # Simuler chaque période d'investissement
    for periode in range(1, nb_periodes + 1):
        valeur_portefeuille += contribution
        contribution_totale += contribution
        valeur_portefeuille = valeur_portefeuille * (1 + rendement_periode - frais_par_periode)
        date_actuelle = date_actuelle + delta_periode
        
        if periode % periode_par_an == 0:
            donnees_annuelles.append({
                'annee': periode // periode_par_an,
                'date': date_actuelle.strftime('%Y-%m-%d'),
                'valeur': round(valeur_portefeuille, 2),
                'contributions': round(montant_initial + contribution_totale, 2),
                'gain': round(valeur_portefeuille - (montant_initial + contribution_totale), 2)
            })
    # Retourner les résultats de la simulation
    # Calculer le CAGR pour investissement DCA
    contribution_mensuelle = contribution if frequence == 1 else contribution * (12 / periode_par_an)
    cagr_dca = calculer_cagr_dca(montant_initial, contribution_mensuelle, valeur_portefeuille, duree_annees)
    
    resultat = {
        'valeur_finale': round(valeur_portefeuille, 2),
        'montant_investi': round(montant_initial + contribution_totale, 2),
        'gain_total': round(valeur_portefeuille - (montant_initial + contribution_totale), 2),
        'rendement_total': round((valeur_portefeuille - (montant_initial + contribution_totale)) / (montant_initial + contribution_totale) * 100, 2),
        'cagr': round(cagr_dca * 100, 2),
        'contribution_totale': round(contribution_totale + montant_initial, 2),
        'donnees_annuelles': donnees_annuelles
    }
    return nettoyer_donnees(resultat)

def calculer_rendements_periode(donnees_annuelles):
    """
    Calcule les rendements annuels et mensuels détaillés
    """
    rendements_annuels = []
    
    for i, annee in enumerate(donnees_annuelles):
        # Vérifier que les valeurs ne sont pas None
        valeur = annee.get('valeur') or 0
        contributions = annee.get('contributions') or 0
        
        if i == 0:
            # Première année : comparer à l'investissement initial
            if contributions > 0:
                rendement = ((valeur - contributions) / contributions) * 100
            else:
                rendement = 0
        else:
            # Années suivantes : comparer au capital de l'année précédente + nouvelles contributions
            valeur_precedente = donnees_annuelles[i-1].get('valeur') or 0
            contributions_precedentes = donnees_annuelles[i-1].get('contributions') or 0
            nouvelles_contributions = contributions - contributions_precedentes
            capital_debut = valeur_precedente + nouvelles_contributions
            
            if capital_debut > 0:
                rendement = ((valeur - capital_debut) / capital_debut) * 100
            else:
                rendement = 0
        
        # Vérifier que le rendement est valide
        if math.isnan(rendement) or math.isinf(rendement):
            rendement = 0
        
        rendements_annuels.append({
            'annee': annee.get('annee', i + 1),
            'rendement_annuel': round(rendement, 2)
        })
    
    return nettoyer_donnees(rendements_annuels)

def calculer_impact_inflation(valeur_finale, montant_investi, nb_annees, taux_inflation=0.02):
    """
    Calcule l'impact de l'inflation sur le portefeuille
    """
    # Valeur réelle ajustée à l'inflation
    valeur_reelle = valeur_finale / ((1 + taux_inflation) ** nb_annees)
    
    # Rendement réel (après inflation)
    gain_reel = valeur_reelle - montant_investi
    rendement_reel = (gain_reel / montant_investi) * 100 if montant_investi > 0 else 0
    
    # Perte due à l'inflation
    perte_inflation = valeur_finale - valeur_reelle
    
    resultat = {
        'valeur_nominale': round(valeur_finale, 2),
        'valeur_reelle': round(valeur_reelle, 2),
        'perte_inflation': round(perte_inflation, 2),
        'rendement_reel': round(rendement_reel, 2),
        'taux_inflation_utilise': taux_inflation * 100
    }
    return nettoyer_donnees(resultat)

def comparer_avec_indice(montant_initial, contribution, frequence, prix_portefeuille, prix_indice, frais_annuels=0):
    """
    Compare la performance du portefeuille avec un indice de référence (ACWI IMI)
    Simule le même investissement DCA sur l'indice
    """
    # Simuler l'investissement sur l'indice
    simulation_indice = simuler_investissement_dca_historique(
        montant_initial, contribution, frequence, prix_indice, frais_annuels
    )
    
    # Simuler l'investissement sur le portefeuille
    simulation_portefeuille = simuler_investissement_dca_historique(
        montant_initial, contribution, frequence, prix_portefeuille, frais_annuels
    )
    
    # Calculer la surperformance / sous-performance
    difference_valeur = simulation_portefeuille['valeur_finale'] - simulation_indice['valeur_finale']
    difference_pct = (difference_valeur / simulation_indice['valeur_finale']) * 100 if simulation_indice['valeur_finale'] > 0 else 0
    
    # Calculer la différence de CAGR
    difference_cagr = simulation_portefeuille['cagr'] - simulation_indice['cagr']
    
    # Créer les données journalières de comparaison
    donnees_comparaison_journalieres = []
    for i in range(min(len(simulation_portefeuille['donnees_mensuelles']), 
                      len(simulation_indice['donnees_mensuelles']))):
        donnees_comparaison_journalieres.append({
            'date': simulation_portefeuille['donnees_mensuelles'][i]['date'],
            'portefeuille': simulation_portefeuille['donnees_mensuelles'][i]['valeur'],
            'indice': simulation_indice['donnees_mensuelles'][i]['valeur'],
            'ecart': round(simulation_portefeuille['donnees_mensuelles'][i]['valeur'] - 
                          simulation_indice['donnees_mensuelles'][i]['valeur'], 2)
        })
    
    resultat = {
        'portefeuille': {
            'valeur_finale': simulation_portefeuille['valeur_finale'],
            'cagr': simulation_portefeuille['cagr'],
            'rendement_total': simulation_portefeuille['rendement_total']
        },
        'indice': {
            'nom': 'ACWI IMI',
            'valeur_finale': simulation_indice['valeur_finale'],
            'cagr': simulation_indice['cagr'],
            'rendement_total': simulation_indice['rendement_total']
        },
        'comparaison': {
            'difference_valeur': round(difference_valeur, 2),
            'difference_pourcentage': round(difference_pct, 2),
            'difference_cagr': round(difference_cagr, 2),
            'surperformance': difference_valeur > 0
        },
        'donnees_comparaison': donnees_comparaison_journalieres
    }
    return nettoyer_donnees(resultat)

def predire_regression_lineaire(X, y, X_pred):
    #Prédit des valeurs en utilisant la régression linéaire
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X_pred)
    return y_pred

def predire_avec_volatilite(X, y, date_debut, date_fin, nb_annees_futures=10):
    """
    Prédit des valeurs journalières avec régression linéaire et calcule les bandes de volatilité
    Retourne les prédictions journalières avec sigma +/- 1 et +/- 2
    date_debut : date de début de la simulation
    date_fin : date de fin de la simulation (pour calculer les dates futures à partir de là)
    """
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    
    # Entraîner le modèle de régression
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculer les résidus pour estimer la volatilité
    y_train_pred = model.predict(X)
    residus = y - y_train_pred
    
    # Écart-type des résidus (volatilité)
    sigma = np.std(residus)
    
    # Dernière année des données historiques
    derniere_annee = int(X[-1][0])
    
    # Convertir les dates en datetime si nécessaire
    if isinstance(date_debut, str):
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d')
    elif hasattr(date_debut, 'to_pydatetime'):
        date_debut = date_debut.to_pydatetime()
    
    if isinstance(date_fin, str):
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d')
    elif hasattr(date_fin, 'to_pydatetime'):
        date_fin = date_fin.to_pydatetime()
    
    # Créer les prédictions journalières pour les années futures
    predictions_avec_bandes = []
    nb_jours_total = nb_annees_futures * 252  # ~252 jours de bourse par an
    
    for jour in range(1, nb_jours_total + 1):
        # Calculer l'année fractionnaire (en jours de bourse)
        annee_fractionnaire = derniere_annee + (jour / 252.0)
        X_pred = np.array([[annee_fractionnaire]])
        pred = model.predict(X_pred)[0]
        
        # Calculer la date future (à partir de date_fin + jours)
        # Approximation : ajouter des jours (incluant weekends, sera filtré par les jours de bourse réels)
        date_future = date_fin + timedelta(days=jour * 365 // 252)
        
        predictions_avec_bandes.append({
            'date': date_future.strftime('%Y-%m-%d'),
            'valeur_predite': float(pred),
            'sigma_plus_1': float(pred + sigma),
            'sigma_plus_2': float(pred + 2 * sigma),
            'sigma_moins_1': float(pred - sigma),
            'sigma_moins_2': float(pred - 2 * sigma)
        })
    
    return nettoyer_donnees(predictions_avec_bandes), float(sigma)

def calculer_histogramme_rendements(donnees_mensuelles):
    """
    Calcule les rendements annuels pour créer un histogramme
    Retourne les rendements par année avec les meilleures et pires années
    """
    if len(donnees_mensuelles) < 2:
        return {'rendements_annuels': [], 'meilleures_annees': [], 'pires_annees': []}
    
    # Grouper les données par année
    from datetime import datetime
    rendements_par_annee = {}
    valeurs_par_annee = {}
    
    for donnee in donnees_mensuelles:
        date = datetime.strptime(donnee['date'], '%Y-%m-%d')
        annee = date.year
        
        if annee not in valeurs_par_annee:
            valeurs_par_annee[annee] = []
        valeurs_par_annee[annee].append(donnee['valeur'])
    
    # Calculer le rendement annuel pour chaque année
    annees_triees = sorted(valeurs_par_annee.keys())
    rendements_annuels = []
    
    for i, annee in enumerate(annees_triees):
        valeur_debut = valeurs_par_annee[annee][0]
        valeur_fin = valeurs_par_annee[annee][-1]
        
        if i > 0:
            # Prendre la dernière valeur de l'année précédente comme référence
            annee_precedente = annees_triees[i-1]
            valeur_debut = valeurs_par_annee[annee_precedente][-1]
        
        if valeur_debut > 0:
            rendement = ((valeur_fin - valeur_debut) / valeur_debut) * 100
        else:
            rendement = 0
        
        rendements_annuels.append({
            'annee': int(annee),
            'rendement': round(rendement, 2)
        })
    
    # Identifier les 3 meilleures et 3 pires années
    rendements_tries = sorted(rendements_annuels, key=lambda x: x['rendement'], reverse=True)
    meilleures_annees = rendements_tries[:3]
    pires_annees = rendements_tries[-3:][::-1]  # Inverser pour avoir du moins pire au pire
    
    resultat = {
        'rendements_annuels': rendements_annuels,
        'meilleures_annees': meilleures_annees,
        'pires_annees': pires_annees
    }
    
    return nettoyer_donnees(resultat)

def simuler_lump_sum(montant_initial, prix_historiques, frais_annuels=0):
    """
    Simule un investissement Lump Sum (montant unique au début) avec données journalières
    """
    date_debut = prix_historiques.index[0].to_pydatetime()
    date_fin = prix_historiques.index[-1].to_pydatetime()
    
    # Frais de gestion
    frais_annuels_decimal = frais_annuels / 100
    frais_par_jour = frais_annuels_decimal / 365
    
    # Investissement initial
    prix_initial = prix_historiques.iloc[0]
    parts_detenues = montant_initial / prix_initial
    
    donnees_journalieres = []
    
    # Suivre l'évolution journalière
    for date_actuelle in prix_historiques.index:
        date_py = date_actuelle.to_pydatetime()
        prix_jour = prix_historiques.loc[date_actuelle]
        
        if pd.isna(prix_jour):
            continue
        
        # Appliquer les frais de gestion journaliers
        parts_detenues = parts_detenues * (1 - frais_par_jour)
        
        # Calculer la valeur du portefeuille
        valeur_portefeuille = parts_detenues * prix_jour
        
        donnees_journalieres.append({
            'date': date_py.strftime('%Y-%m-%d'),
            'valeur': round(valeur_portefeuille, 2) if valeur_portefeuille is not None else 0
        })
    
    valeur_finale = donnees_journalieres[-1]['valeur'] if donnees_journalieres else montant_initial
    duree_annees = (date_fin - date_debut).days / 365.25
    cagr = calculer_cagr(montant_initial, valeur_finale, duree_annees)
    
    resultat = {
        'valeur_finale': round(valeur_finale, 2),
        'montant_investi': montant_initial,
        'gain_total': round(valeur_finale - montant_initial, 2),
        'rendement_total': round((valeur_finale - montant_initial) / montant_initial * 100, 2) if montant_initial > 0 else 0,
        'cagr': round(cagr * 100, 2),
        'donnees_mensuelles': donnees_journalieres
    }
    
    return nettoyer_donnees(resultat)
