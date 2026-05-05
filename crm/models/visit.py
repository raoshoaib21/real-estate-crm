from django.db import models
from django.conf import settings
from crm.models.lead import Lead
from crm.models.property import Property


class SiteVisit(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    visit_id = models.CharField(max_length=20, unique=True, editable=False)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='visits')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='visits')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='visits')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True)
    lead_interested = models.BooleanField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_date', '-scheduled_time']

    def __str__(self):
        return f"{self.visit_id} - {self.lead.full_name}"

    def save(self, *args, **kwargs):
        if not self.visit_id:
            last = SiteVisit.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.visit_id = f"VISIT-{num:06d}"
        super().save(*args, **kwargs)
