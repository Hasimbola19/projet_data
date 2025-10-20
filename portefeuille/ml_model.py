import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression

def download_rendements(ticker,periode,freq):
  data=yf.download(ticker,period=periode,interval=freq) 
  #calcul des rendements 
  data['rendements']=np.
  rendements=data['rendement'].dropna().values
return rendements
def regression_lineaire(rendements,periode_future):
  X=np.arrange(len(rendements)).reshape(-1,1)
  y=rendements 

  model=LinerRegression()
  model.fit(X,y)
  predict_exist=model.predict(X)
  residus=y-predict_exist
  ecart_type_residus=np.std(residus)
    
return 
