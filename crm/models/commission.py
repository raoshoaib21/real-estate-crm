from django.db import models
from django.conf import settings
from crm.models.deal import Deal


class Commission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ]

    deal = models.ForeignKey(Deal, on_delete=models.PROTECT, related_name='commissions')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commissions')
    deal_value = models.DecimalField(max_digits=12, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Commission rate (%)")
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Calculated commission")
    split_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='split_commissions', help_text="Co-broke agent")
    split_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100, help_text="Agent's share (%)")
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="After split")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agent.get_full_name()} - {self.deal.deal_id}"

    def save(self, *args, **kwargs):
        self.commission_amount = self.deal_value * (self.commission_rate / 100)
        self.net_amount = self.commission_amount * (self.split_percentage / 100)
        super().save(*args, **kwargs)
