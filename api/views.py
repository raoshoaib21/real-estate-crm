from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from crm.models.user import CustomUser
from crm.models.property import Property
from crm.models.lead import Lead
from crm.models.deal import Deal, PipelineStage
from crm.models.visit import SiteVisit
from crm.models.commission import Commission
from api.serializers import (
    UserSerializer, PropertySerializer, LeadSerializer,
    DealSerializer, PipelineStageSerializer, SiteVisitSerializer,
    CommissionSerializer,
)


class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-listed_date')
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        city = self.request.query_params.get('city')
        if status:
            qs = qs.filter(status=status)
        if city:
            qs = qs.filter(city__icontains=city)
        return qs


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        lead_type = self.request.query_params.get('type')
        if status:
            qs = qs.filter(status=status)
        if lead_type:
            qs = qs.filter(lead_type=lead_type)
        if self.request.user.is_agent:
            qs = qs.filter(assigned_to=self.request.user)
        return qs


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all().order_by('-created_at')
    serializer_class = DealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        stage = self.request.query_params.get('stage')
        if stage:
            qs = qs.filter(stage__name=stage)
        if self.request.user.is_agent:
            qs = qs.filter(agent=self.request.user)
        return qs


class PipelineStageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PipelineStage.objects.all().order_by('order')
    serializer_class = PipelineStageSerializer
    permission_classes = [permissions.IsAuthenticated]


class SiteVisitViewSet(viewsets.ModelViewSet):
    queryset = SiteVisit.objects.all().order_by('-scheduled_date')
    serializer_class = SiteVisitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        if self.request.user.is_agent:
            qs = qs.filter(agent=self.request.user)
        return qs


class CommissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Commission.objects.all().order_by('-created_at')
    serializer_class = CommissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_agent:
            qs = qs.filter(agent=self.request.user)
        return qs

    @action(detail=False, methods=['get'])
    def summary(self, request):
        qs = self.get_queryset()
        total_pending = qs.filter(status='pending').aggregate_total('net_amount') or 0
        total_paid = qs.filter(status='paid').aggregate_total('net_amount') or 0
        return Response({
            'total_pending': float(total_pending),
            'total_paid': float(total_paid),
        })
