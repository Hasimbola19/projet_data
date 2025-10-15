from django.urls import path, include
from rest_framework import routers
from .views import PortefeuilleCalculatorView

router = routers.DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/calcul-portefeuille/', PortefeuilleCalculatorView.as_view(), name='calcul-sharpe'),
]