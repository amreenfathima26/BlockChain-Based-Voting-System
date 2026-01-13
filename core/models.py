from django.contrib.auth.models import AbstractUser
from django.db import models
import hashlib
import json
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('voter', 'Voter'),
        ('candidate', 'Candidate'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='voter')
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} ({self.role})"

class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField()  # JSON string of vote data
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
    nonce = models.IntegerField(default=0)
    
    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __str__(self):
        return f"Block {self.index}"

class SiteConfiguration(models.Model):
    # Global Settings
    site_name = models.CharField(max_length=255, default="SecureVote Blockchain")
    groq_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="Enter GROQ API Key here to override environment variable")
    
    # Theme Customization (Hex Colors)
    # Admin (Default: Deep Purple/Slate)
    admin_primary_color = models.CharField(max_length=20, default="#0f172a") 
    admin_secondary_color = models.CharField(max_length=20, default="#1e293b")
    
    # Voter (Default: Teal/Emerald)
    voter_primary_color = models.CharField(max_length=20, default="#064e3b") 
    voter_secondary_color = models.CharField(max_length=20, default="#065f46")
    
    # Candidate (Default: Amber/Orange)
    candidate_primary_color = models.CharField(max_length=20, default="#7c2d12")
    candidate_secondary_color = models.CharField(max_length=20, default="#9a3412")

    # System Controls
    maintenance_mode = models.BooleanField(default=False, help_text="If active, only Superadmin can access the site")
    allow_registration = models.BooleanField(default=True, help_text="Allow new users to register")
    security_encryption_active = models.BooleanField(default=False, help_text="Global switch for the Security Indicator Box")
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True, help_text="Upload a custom favicon (PNG/ICO)")
    
    # Fake Stats for Admin Dashboard
    voter_participation_rate = models.IntegerField(default=45, help_text="Percentage (0-100) to display in Election Health")
    system_load_percentage = models.IntegerField(default=12, help_text="Percentage (0-100) to display in System Load")

    def save(self, *args, **kwargs):
        self.pk = 1 # Force singleton
        super(SiteConfiguration, self).save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Global Site Configuration"
