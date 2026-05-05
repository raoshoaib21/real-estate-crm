from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    UserViewSet, PropertyViewSet, LeadViewSet,
    DealViewSet, PipelineStageViewSet, SiteVisitViewSet,
    CommissionViewSet,
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('properties', PropertyViewSet)
router.register('leads', LeadViewSet)
router.register('deals', DealViewSet)
router.register('pipeline-stages', PipelineStageViewSet)
router.register('visits', SiteVisitViewSet)
router.register('commissions', CommissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
