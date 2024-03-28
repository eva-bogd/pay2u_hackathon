from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionViewSet, TariffViewSet, UserTariffViewSet

router_api_v1 = DefaultRouter()

router_api_v1.register(r'^services', SubscriptionViewSet, basename='services')
router_api_v1.register(r'^tariffs', TariffViewSet, basename='tariffs')
router_api_v1.register(r'^usertariffs',
                       UserTariffViewSet,
                       basename='usertariffs')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
