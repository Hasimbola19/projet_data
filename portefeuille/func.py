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

def simuler_investissement_dca(montant_initial, contribution, frequence, duree_annees, rendement_annuel, frais_annuels=0):
    #Simule un investissement en DCA (Dollar-Cost Averaging)
    if frequence == 1:
        periode_par_an = 12
    elif frequence == 2:
        periode_par_an = 4
    elif frequence == 4:
        periode_par_an = 2
    else:
        periode_par_an = 1

    nb_periodes = duree_annees * periode_par_an 
    rendement_periode = (1 + rendement_annuel) ** (1 / periode_par_an) - 1
    frais_par_periode = (1 + frais_annuels) ** (1 / periode_par_an) - 1

    valeur_portefeuille = montant_initial
    contribution_totale = 0
    donnees_annuelles = []
    
    for periode in range(1, nb_periodes + 1):
        valeur_portefeuille += contribution
        contribution_totale += contribution
        valeur_portefeuille = valeur_portefeuille * (1 + rendement_periode) * (1 - frais_par_periode)
        if periode % periode_par_an == 0:
            donnees_annuelles.append({
                'annee': periode // periode_par_an,
                'valeur': round(valeur_portefeuille, 2),
                'contributions': round(montant_initial + contribution_totale, 2),
                'gain': round(valeur_portefeuille - (montant_initial + contribution_totale), 2)
            })
    return {
        'valeur_finale': round(valeur_portefeuille, 2),
        'montant_investi': round(montant_initial + contribution_totale, 2),
        'gain_total': round(valeur_portefeuille - (montant_initial + contribution_totale), 2),
        'rendement_total': round((valeur_portefeuille - (montant_initial + contribution_totale)) / (montant_initial + contribution_totale) * 100, 2),
        'cagr': round(calculer_cagr(montant_initial, valeur_portefeuille, duree_annees) * 100, 2),
        'contribution_totale': round(contribution_totale + montant_initial, 2),
        'donnees_annuelles': donnees_annuelles
    }

def predire_regression_lineaire(X, y, X_pred):
    #Prédit des valeurs en utilisant la régression linéaire
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X_pred)
    return y_pred
