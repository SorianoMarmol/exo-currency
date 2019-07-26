from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'CurrencyRates', views.CurrencyRatesWS)

api_urlpatterns = router.urls
