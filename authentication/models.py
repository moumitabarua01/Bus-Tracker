from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date

def validate_birth_date(value):
    """Validate that birth date is not in the future and user is at least 13 years old."""
    if value > date.today():
        raise ValidationError('Birth date cannot be in the future.')
    
    age = (date.today() - value).days // 365
    if age < 13:
        raise ValidationError('You must be at least 13 years old to register.')

class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, help_text='Tell us about yourself (max 500 characters)')
    location = models.CharField(
        max_length=100, 
        blank=True, 
        help_text='Your current location',
        validators=[RegexValidator(
            message='Location can only contain letters, spaces, hyphens, commas, and periods',
            regex='^[a-zA-Z\\s\\-,\\.]+$'
        )]
    )
    birth_date = models.DateField(
        null=True, 
        blank=True, 
        help_text='Your date of birth',
        validators=[validate_birth_date]
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True,
        help_text='Upload a profile picture (JPG, PNG, GIF)',
        validators=[RegexValidator(
            message='Only JPG, PNG, and GIF files are allowed',
            regex='^.*\\.(jpg|jpeg|png|gif)$',
            flags=0
        )]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    emergency_contact = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text='Emergency contact name'
    )
    emergency_phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text='Emergency contact phone number',
        validators=[RegexValidator(
            message='Emergency phone number must be entered in the format: "+999999999". Up to 15 digits allowed.',
            regex='^\\+?1?\\d{9,15}$'
        )]
    )
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text='Your phone number (optional)',
        validators=[RegexValidator(
            message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.',
            regex='^\\+?1?\\d{9,15}$'
        )]
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user'], name='authenticat_user_id_35f8a3_idx'),
            models.Index(fields=['is_verified'], name='authenticat_is_veri_bf7dac_idx'),
        ]
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
