from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, BranchViewSet, WarehouseViewSet
from .views import CompanyViewSet, BranchViewSet, WarehouseViewSet, TerminalViewSet
from .pos_settings_views import POSFBRSettingsViewSet
 
router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"branches", BranchViewSet, basename="branch")
router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
router.register(r"terminals", TerminalViewSet, basename="terminal")
router.register(r"pos-fbr-settings", POSFBRSettingsViewSet, basename="pos-fbr-settings")
 
urlpatterns = [
    path("", include(router.urls)),
]