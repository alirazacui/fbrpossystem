from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, BranchViewSet, WarehouseViewSet
from .views import CompanyViewSet, BranchViewSet, WarehouseViewSet, TerminalViewSet
 
router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"branches", BranchViewSet, basename="branch")
router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
router.register(r"terminals", TerminalViewSet, basename="terminal")
 
urlpatterns = [
    path("", include(router.urls)),
]