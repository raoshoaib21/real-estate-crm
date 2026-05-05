from django.db import models
from django.conf import settings


class LeadSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Cost per lead")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Lead(models.Model):
    TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('renter', 'Renter'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('walk_in', 'Walk-in'),
        ('social', 'Social Media'),
        ('portal', 'Property Portal'),
        ('cold_call', 'Cold Call'),
        ('email_campaign', 'Email Campaign'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('hot', 'Hot'),
    ]

    lead_id = models.CharField(max_length=20, unique=True, editable=False)
    lead_type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website')
    custom_source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    expected_sell_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    preferred_location = models.CharField(max_length=200, blank=True)
    preferred_type = models.CharField(max_length=20, choices=[('any', 'Any')] + [
        ('apartment', 'Apartment'), ('house', 'House'), ('villa', 'Villa'),
        ('commercial', 'Commercial'), ('land', 'Land'), ('plot', 'Plot'),
    ], default='any')
    requirements = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    lead_score = models.PositiveIntegerField(default=0, help_text="Auto-calculated 0-100")
    created_at = models.DateTimeField(auto_now_add=True)
    last_contacted = models.DateTimeField(blank=True, null=True)
    converted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.lead_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.lead_id:
            last = Lead.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.lead_id = f"LEAD-{num:06d}"
        self.calculate_score()
        super().save(*args, **kwargs)

    def calculate_score(self):
        score = 0
        if self.priority == 'hot':
            score += 40
        elif self.priority == 'high':
            score += 30
        elif self.priority == 'medium':
            score += 20
        else:
            score += 10

        if self.budget_max and self.budget_min:
            score += 20
        if self.phone:
            score += 10
        if self.email:
            score += 10
        if self.lead_type == 'buyer' and self.preferred_location:
            score += 10
        if self.status in ['qualified', 'proposal', 'negotiation']:
            score += 10

        self.lead_score = min(score, 100)
