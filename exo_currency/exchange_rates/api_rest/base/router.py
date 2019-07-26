from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'CurrencyRates', views.CurrencyRatesWS, basename='currency_rates')

api_urlpatterns = [
    path(r'currency_rates/', views.CurrencyRatesWS.as_view()),
    path(r'calculate_amount/', views.CalculateAmountWS.as_view()),
    path(r'TWR/', views.TimeWeightedRateWS.as_view()),
]

api_urlpatterns += router.urls
