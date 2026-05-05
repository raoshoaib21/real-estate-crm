from rest_framework import serializers
from crm.models.user import CustomUser
from crm.models.property import Property, PropertyImage
from crm.models.lead import Lead
from crm.models.deal import Deal, PipelineStage
from crm.models.visit import SiteVisit
from crm.models.commission import Commission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'phone', 'commission_rate']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_primary', 'caption']


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    listed_by_name = serializers.CharField(source='listed_by.get_full_name', read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['listing_id']


class LeadSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['lead_id', 'lead_score']


class PipelineStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineStage
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.full_name', read_only=True)
    property_title = serializers.CharField(source='deal_property.title', read_only=True)
    agent_name = serializers.CharField(source='agent.get_full_name', read_only=True)
    stage_name = serializers.CharField(source='stage.name', read_only=True)
    probability = serializers.IntegerField(read_only=True)
    weighted_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Deal
        fields = '__all__'
        read_only_fields = ['deal_id']


class SiteVisitSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.full_name', read_only=True)
    property_title = serializers.CharField(source='property.title', read_only=True)
    agent_name = serializers.CharField(source='agent.get_full_name', read_only=True)

    class Meta:
        model = SiteVisit
        fields = '__all__'
        read_only_fields = ['visit_id']


class CommissionSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.get_full_name', read_only=True)
    deal_id = serializers.CharField(source='deal.deal_id', read_only=True)

    class Meta:
        model = Commission
        fields = '__all__'
