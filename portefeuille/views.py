import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SharpeInputSerializer

class PortefeuilleCalculatorView(APIView):
    #récupere les données de l'utilisateyr via la requete post
    def post(self, request):
        serializer = SharpeInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
#calcul du rendement, volatilite, ratio de sharpe..
            rendements = np.array(data.get("rendements", []))
            risk_free_rate = data.get("risk_free_rate", 0.01)
            actifs = data.get("actifs", [])
            etfs_populaires = data.get("etfs_populaires", [])
            duree = data.get("duree_investissement", 10)
            frais = float(data.get("frais_gestion_annuels")) / 100
            montant_initial = float(data.get("montant_initial_investissement"))
            contribution = float(data.get("montant_contribution_recurrente"))
            frequence = data.get("frequence_contribution", 1)

            if len(rendements) < 2:
                return Response(
                    {"error": "Il faut au moins deux rendements pour calculer la volatilité."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Calcul du rendement moyen et de la volatilité
            expected_return = float(np.mean(rendements))
            volatility = float(np.std(rendements, ddof=1))
            sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else None

            # Projection annuelle
            valeurs_annuelles = []
            valeur = montant_initial

            if frequence == 1 : # mensuelle
                contribution_annuelle = contribution * 12
            elif frequence == 2 : # trimestrielle
                contribution_annuelle = contribution * 4
            else :
                contribution_annuelle = contribution

            total_contrib = 0

            for annee in range(1, duree + 1):
                total_contrib += contribution_annuelle
                valeur = (valeur + contribution_annuelle) * (1 + expected_return - frais)
                gain_net = valeur - (montant_initial + total_contrib)
                valeurs_annuelles.append({
                    "annee": annee,
                    "valeur": round(valeur, 2),
                    "contributions_cumulees": round(total_contrib, 2),
                    "gain_net": round(gain_net, 2)
                })

            # Intervalles statistiques (règle 68-95-99.7 %)
            interval_68 = [expected_return - volatility, expected_return + volatility]
            interval_95 = [expected_return - 2*volatility, expected_return + 2*volatility]
            interval_997 = [expected_return - 3*volatility, expected_return + 3*volatility]

            return Response({
                "actifs_selectionnes": actifs,
                "etfs_populaires": etfs_populaires,
                "expected_return": round(expected_return, 6),
                "volatility": round(volatility, 6),
                "sharpe_ratio": round(sharpe_ratio, 6) if sharpe_ratio else None,
                "intervals_volatilite": {
                    "68%": [round(interval_68[0], 6), round(interval_68[1], 6)],
                    "95%": [round(interval_95[0], 6), round(interval_95[1], 6)],
                    "99.7%": [round(interval_997[0], 6), round(interval_997[1], 6)]
                },
                "valeurs_annuelles": valeurs_annuelles,
                "interpretation": (
                    "Selon la loi normale :\n"
                    "- 68% des rendements dans ±1σ\n"
                    "- 95% dans ±2σ\n"
                    "- 99,7% dans ±3σ\n"
                    "Plus la volatilité est forte, plus le risque de fluctuation est élevé."
                )
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
