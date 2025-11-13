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
    #Télécharge les données historiques depuis Yahoo Finance
    try:
        etf = yf.Ticker(ticker)
        return etf.history(period=periode)
    except:
        return pd.DataFrame()
def calculer_rendements(prix):
    #Calcule les rendements quotidiens à partir des prix de clôture ajustés
    return prix['Close'].pct_change().dropna()  
def calculer_volatilite(rendements, annualiser=True):
    #Calcule la volatilité des rendements
    volatilite = rendements.std()
    if annualiser:
        volatilite *= (252 ** 0.5)  # Annualisation pour les rendements quotidiens
    return volatilite

def calculer_rendement_moyen(rendements, annualiser=True):
    #Calcule le rendement moyen des rendements
    rendement_moyen = rendements.mean()
    if annualiser:
        rendement_moyen *= 252  # Annualisation pour les rendements quotidiens
    return rendement_moyen          
def calculer_sharpe_ratio(rendements, risk_free_rate=0.02): 
    #Calcule le Sharpe Ratio
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
    nb_periodes = duree_annees * frequence
    valeur_portefeuille = montant_initial
    for periode in range(1, nb_periodes + 1):
        valeur_portefeuille *= (1 + rendement_annuel / frequence)
        valeur_portefeuille += contribution
        valeur_portefeuille *= (1 - frais_annuels / frequence)
    return valeur_portefeuille
def predire_regression_lineaire(X, y, X_pred):
    #Prédit des valeurs en utilisant la régression linéaire
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X_pred)
    return y_pred
