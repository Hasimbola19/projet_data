#import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression

'''  telecharger_donnees_marche(ticker, periode="5y")
    calculer_rendements(prix)
    calculer_volatilite(rendements, annualiser=True)
    calculer_rendement_moyen(rendements, annualiser=True)
    calculer_sharpe_ratio(rendements, risk_free_rate=0.02) // on a besoin de rendement et de volatilité
    calculer_cagr(valeur_initiale, valeur_finale, nb_annees)
    simuler_investissement_dca(montant_initial, contribution, frequence, duree_annees, rendement_annuel, frais_annuels=0)
    predire_regression_lineaire(X, y, X_pred)
'''
def telecharger_donnees_marche(ticker, periode="5y"):
    #Téléchargement des données historiques depuis Yahoo Finance
    try:
        etf = yf.Ticker(ticker)
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

def calculer_sharpe_ratio(rendements, risk_free_rate=0.02): 
    #Calcule leratio de sharp
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
    Calcule le CAGR pour un investissement DCA en utilisant la méthode IRR/XIRR
    Cette méthode calcule le taux de rendement interne réel
    """
    if nb_annees <= 0:
        return 0
    
    # Méthode itérative pour trouver l'IRR (Internal Rate of Return)
    # On cherche le taux r tel que VAN = 0
    from scipy.optimize import newton
    
    def npv(taux):
        # Valeur actuelle nette des flux de trésorerie
        total = -montant_initial  # Investissement initial (sortie)
        
        # Contributions mensuelles
        for mois in range(1, int(nb_annees * 12) + 1):
            total -= contribution_mensuelle / ((1 + taux) ** (mois / 12))
        
        # Valeur finale (entrée)
        total += valeur_finale / ((1 + taux) ** nb_annees)
        
        return total
    
    try:
        # Trouver le taux qui rend la VAN = 0
        irr = newton(npv, 0.05)  # Estimation initiale de 5%
        return irr
    except:
        # Si la méthode échoue, utiliser la formule approximative
        total_contributions = montant_initial + (contribution_mensuelle * 12 * nb_annees)
        valeur_moyenne_investie = montant_initial + (total_contributions - montant_initial) / 2
        
        if valeur_moyenne_investie <= 0:
            return 0
        
        cagr = (valeur_finale / valeur_moyenne_investie) ** (1 / nb_annees) - 1
        return cagr

def simuler_investissement_dca_historique(montant_initial, contribution, frequence, prix_historiques, frais_annuels=0):
    """
    Simule un investissement DCA en utilisant les prix historiques réels
    prix_historiques : pandas Series avec les prix et les dates en index
    """
    from dateutil.relativedelta import relativedelta
    
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
    frais_par_periode = frais_annuels_decimal / periode_par_an
    
    # Initialisation
    date_debut = prix_historiques.index[0].to_pydatetime()
    date_fin = prix_historiques.index[-1].to_pydatetime()
    
    valeur_portefeuille = 0
    parts_detenues = 0
    contribution_totale = 0
    donnees_annuelles = []
    
    date_actuelle = date_debut
    periode = 0
    annee_actuelle = 0
    
    # Premier investissement
    prix_actuel = prix_historiques.iloc[0]
    parts_detenues = montant_initial / prix_actuel
    contribution_totale = montant_initial
    
    # Simuler chaque période
    while date_actuelle <= date_fin:
        periode += 1
        date_actuelle = date_actuelle + delta_periode
        
        # Trouver le prix le plus proche de la date
        try:
            prix_proche = prix_historiques.asof(date_actuelle)
            if pd.isna(prix_proche):
                continue
                
            # Ajouter la contribution et acheter des parts
            if contribution > 0:
                parts_achetees = contribution / prix_proche
                parts_detenues += parts_achetees
                contribution_totale += contribution
            
            # Appliquer les frais de gestion (réduire les parts)
            parts_detenues = parts_detenues * (1 - frais_par_periode)
            
            # Calculer la valeur du portefeuille
            valeur_portefeuille = parts_detenues * prix_proche
            
            # Enregistrer les données annuelles
            if periode % periode_par_an == 0:
                annee_actuelle += 1
                donnees_annuelles.append({
                    'annee': annee_actuelle,
                    'date': date_actuelle.strftime('%Y-%m-%d'),
                    'valeur': round(valeur_portefeuille, 2),
                    'contributions': round(contribution_totale, 2),
                    'gain': round(valeur_portefeuille - contribution_totale, 2)
                })
        except:
            continue
    
    # Calculer le CAGR réel
    duree_annees = (date_fin - date_debut).days / 365.25
    contribution_mensuelle = contribution if frequence == 1 else contribution * (12 / periode_par_an)
    cagr_dca = calculer_cagr_dca(montant_initial, contribution_mensuelle, valeur_portefeuille, duree_annees)
    
    return {
        'valeur_finale': round(valeur_portefeuille, 2),
        'montant_investi': round(contribution_totale, 2),
        'gain_total': round(valeur_portefeuille - contribution_totale, 2),
        'rendement_total': round((valeur_portefeuille - contribution_totale) / contribution_totale * 100, 2) if contribution_totale > 0 else 0,
        'cagr': round(cagr_dca * 100, 2),
        'contribution_totale': round(contribution_totale, 2),
        'donnees_annuelles': donnees_annuelles
    }

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
    
    return {
        'valeur_finale': round(valeur_portefeuille, 2),
        'montant_investi': round(montant_initial + contribution_totale, 2),
        'gain_total': round(valeur_portefeuille - (montant_initial + contribution_totale), 2),
        'rendement_total': round((valeur_portefeuille - (montant_initial + contribution_totale)) / (montant_initial + contribution_totale) * 100, 2),
        'cagr': round(cagr_dca * 100, 2),
        'contribution_totale': round(contribution_totale + montant_initial, 2),
        'donnees_annuelles': donnees_annuelles
    }

def calculer_rendements_periode(donnees_annuelles):
    """
    Calcule les rendements annuels et mensuels détaillés
    """
    rendements_annuels = []
    
    for i, annee in enumerate(donnees_annuelles):
        if i == 0:
            # Première année : comparer à l'investissement initial
            rendement = ((annee['valeur'] - annee['contributions']) / annee['contributions']) * 100
        else:
            # Années suivantes : comparer au capital de l'année précédente + nouvelles contributions
            valeur_precedente = donnees_annuelles[i-1]['valeur']
            nouvelles_contributions = annee['contributions'] - donnees_annuelles[i-1]['contributions']
            capital_debut = valeur_precedente + nouvelles_contributions
            rendement = ((annee['valeur'] - capital_debut) / capital_debut) * 100 if capital_debut > 0 else 0
        
        rendements_annuels.append({
            'annee': annee['annee'],
            'rendement_annuel': round(rendement, 2)
        })
    
    return rendements_annuels

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
    
    return {
        'valeur_nominale': round(valeur_finale, 2),
        'valeur_reelle': round(valeur_reelle, 2),
        'perte_inflation': round(perte_inflation, 2),
        'rendement_reel': round(rendement_reel, 2),
        'taux_inflation_utilise': taux_inflation * 100
    }

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
    
    return {
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
        'donnees_comparaison': [
            {
                'annee': i + 1,
                'portefeuille': simulation_portefeuille['donnees_annuelles'][i]['valeur'],
                'indice': simulation_indice['donnees_annuelles'][i]['valeur'],
                'ecart': round(simulation_portefeuille['donnees_annuelles'][i]['valeur'] - 
                              simulation_indice['donnees_annuelles'][i]['valeur'], 2)
            }
            for i in range(min(len(simulation_portefeuille['donnees_annuelles']), 
                              len(simulation_indice['donnees_annuelles'])))
        ]
    }

def predire_regression_lineaire(X, y, X_pred):
    #Prédit des valeurs en utilisant la régression linéaire
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X_pred)
    return y_pred
