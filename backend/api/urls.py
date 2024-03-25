from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet

router_api_v1 = DefaultRouter()

router_api_v1.register(
    r'^services',
    SubscriptionViewSet,
    basename='services')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
