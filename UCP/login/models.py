from datetime import timedelta
import os
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from UCP.settings import VERIFICATION_EMAIL_EXPIRY_TIME,PASSWORD_RESET_CODE_EXPIRY_TIME

class UserProfile(models.Model):
    """
    Teachers and student profiles who are portal users.
    """
    DESIGNATION_CHOICES =(
        (0, 'Teacher'),
        (1, 'Student')
    )
    
    user = models.OneToOneField(User, unique=True, related_name='user_login')
    first_name = models.CharField(null=True, max_length=100)
    last_name = models.CharField(null=True, max_length=100)
    designation = models.IntegerField( choices = DESIGNATION_CHOICES, default=0)
    profile_image = models.ImageField(upload_to="/user_images/profile_images", blank=True)

    class Admin:
        list_display = ('first_name','designation')
        search_fields = ('first_name','last_name','designation')

    def __unicode__(self):
        return self.first_name + " " + self.last_name

class EmailVerificationCode(models.Model):
    """
    Codes for verifying user emails after registration
    """
    
    user = models.ForeignKey(User)
    verification_code = models.CharField(blank=True, max_length=100)
    expiry_date = models.DateField()
    
    def set_expiry_date(self):
        return timezone.now()+timedelta(days=VERIFICATION_EMAIL_EXPIRY_TIME)
        
    def create_hash_code(self):
        return os.urandom(32).encode('hex')
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = self.set_expiry_date()
            self.verification_code = self.create_hash_code()
        super(EmailVerificationCode, self).save(*args, **kwargs)

class PasswordResetCode(models.Model):
    """
    Codes for users to recover their accounts
    """
    
    user = models.ForeignKey(User)
    reset_code = models.CharField(blank=True, max_length=100)
    expiry_date = models.DateField()
    
    def set_expiry_date(self):
        return timezone.now()+timedelta(days=PASSWORD_RESET_CODE_EXPIRY_TIME)
        
    def create_hash_code(self):
        return os.urandom(6).encode('hex')
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = self.set_expiry_date()
            self.reset_code = self.create_hash_code()
        super(PasswordResetCode, self).save(*args, **kwargs)
        