from django.urls import path, include
from rest_framework import routers
from .views import SimuerPortefeuilleView
#crée les routes pour l'api
router = routers.DefaultRouter()

urlpatterns = [
    path('api/simuler/', SimuerPortefeuilleView.as_view(), name='simuler-portefeuille'),
]
