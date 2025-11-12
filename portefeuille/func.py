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
    rendement_total = ((prix.iloc[-1] - prix.iloc[0]) / prix.iloc[0]) * 100
    print(f"Rendement total = {rendement_total:.2f}%")
    
print("calcul des rendements",calculer_rendements(pd.Series ([100, 110, 120, 130, 140])))
    #rendements = prix.pct_change().dropna()