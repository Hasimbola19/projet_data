from .models import ETF
# crée les etf populaires 
def creer_etf_populaires():
    etfs = [
        {"nom": "SPDR S&P 500 ETF", "ticker": "SPY"},
        {"nom": "iShares Core MSCI World", "ticker": "IWDA"},
        {"nom": "Vanguard Total Stock Market", "ticker": "VTI"},
        {"nom": "Invesco QQQ Trust", "ticker": "QQQ"},
        {"nom": "Vanguard FTSE All-World", "ticker": "VEVE"},
        {"nom": "iShares MSCI Emerging Markets", "ticker": "EEM"},
        {"nom": "Vanguard S&P 500 ETF", "ticker": "VOO"},
        {"nom": "iShares Core US Aggregate Bond", "ticker": "AGG"},
        {"nom": "SPDR Gold Shares", "ticker": "GLD"},
        {"nom": "Vanguard Total Bond Market", "ticker": "BND"},
    ]

    for etf in etfs:
        ETF.objects.get_or_create(nom=etf["nom"], ticker=etf["ticker"])
