from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('agent', 'Agent'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='agent')
    phone = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True)
    joined_at = models.DateField(auto_now_add=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0, help_text="Default commission rate (%)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_manager(self):
        return self.role in ['admin', 'manager']

    @property
    def is_agent(self):
        return self.role == 'agent'
