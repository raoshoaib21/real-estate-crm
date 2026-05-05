from django.db import models
from django.conf import settings
from crm.models.lead import Lead
from crm.models.property import Property


class PipelineStage(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order = models.PositiveIntegerField(unique=True)
    probability = models.PositiveIntegerField(default=0, help_text="Close probability (%)")
    color = models.CharField(max_length=7, default='#6B7280', help_text="Hex color code")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Deal(models.Model):
    deal_id = models.CharField(max_length=20, unique=True, editable=False)
    lead = models.ForeignKey(Lead, on_delete=models.PROTECT, related_name='deals')
    deal_property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='deals')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deals')
    stage = models.ForeignKey(PipelineStage, on_delete=models.PROTECT, related_name='deals')
    deal_value = models.DecimalField(max_digits=12, decimal_places=2)
    offer_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    counter_offer = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    deal_type = models.CharField(max_length=10, choices=[('sale', 'Sale'), ('rental', 'Rental')], default='sale')
    expected_close_date = models.DateField(blank=True, null=True)
    actual_close_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.deal_id} - {self.lead.full_name}"

    def save(self, *args, **kwargs):
        if not self.deal_id:
            last = Deal.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.deal_id = f"DEAL-{num:06d}"
        super().save(*args, **kwargs)

    @property
    def probability(self):
        return self.stage.probability if self.stage else 0

    @property
    def weighted_value(self):
        return float(self.deal_value) * (self.probability / 100)


class DealActivity(models.Model):
    ACTIVITY_TYPES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('visit', 'Site Visit'),
        ('note', 'Note'),
        ('offer', 'Offer Made'),
        ('counter_offer', 'Counter Offer'),
    ]

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.deal.deal_id}"
