from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('api/public/', include(router.urls)),
]
