from django.db import models
from django.conf import settings


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
        ('plot', 'Plot'),
        ('penthouse', 'Penthouse'),
        ('studio', 'Studio'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('under_offer', 'Under Offer'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('withdrawn', 'Withdrawn'),
    ]

    listing_id = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    negotiable = models.BooleanField(default=True)
    area_sqft = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    amenities = models.JSONField(default=dict, blank=True, help_text='{"pool": true, "garage": true, "garden": false}')
    year_built = models.PositiveIntegerField(blank=True, null=True)
    floor = models.PositiveIntegerField(blank=True, null=True)
    total_floors = models.PositiveIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveIntegerField(default=0)
    listed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='properties')
    featured = models.BooleanField(default=False)
    listed_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-listed_date']

    def __str__(self):
        return f"{self.title} ({self.listing_id})"

    def save(self, *args, **kwargs):
        if not self.listing_id:
            last = Property.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.listing_id = f"PROP-{num:06d}"
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        return img if img else self.images.first()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']

    def __str__(self):
        return f"Image for {self.property.listing_id}"


class PropertyDocument(models.Model):
    DOC_TYPES = [
        ('floor_plan', 'Floor Plan'),
        ('legal', 'Legal Document'),
        ('brochure', 'Brochure'),
        ('other', 'Other'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='property_docs/')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.property.listing_id}"
