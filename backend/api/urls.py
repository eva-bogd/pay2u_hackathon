from django.urls import include, path
from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from .views import (
    SubscriptionViewSet,
    MySubscriptionViewSet,
    TariffViewSet,
    UserTariffViewSet
)

router_api_v1 = DefaultRouter()

router_api_v1.register(r'^services',
                       SubscriptionViewSet,
                       basename='services')
router_api_v1.register(r'^my_subscriptions',
                       MySubscriptionViewSet,
                       basename='my_subscriptions')
router_api_v1.register(r'^tariffs',
                       TariffViewSet,
                       basename='tariffs')
router_api_v1.register(r'^tariffs',
                       UserTariffViewSet,
                       basename='tariffs')

=======
from .views import MySubscriptionViewSet, SubscriptionViewSet, TariffViewSet

router_api_v1 = DefaultRouter()

router_api_v1.register(
    r'^services',
    SubscriptionViewSet,
    basename='services')
router_api_v1.register(
    r'^my_subscriptions',
    MySubscriptionViewSet,
    basename='my_subscriptions')
router_api_v1.register(
    r'^tariffs',
    TariffViewSet,
    basename='tariffs')
>>>>>>> 6cc026655e5860181e19e5fed9f2500648fbc361

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/', include('djoser.urls')),  # Работа с пользователями
    path('v1/', include('djoser.urls.authtoken')),  # Работа с токенами
]
