from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import timedelta
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        get_latest_by = 'updated_at'
        ordering = ('-updated_at', '-created_at',)
        abstract = True



class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = None
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    email_verification_code = models.CharField(max_length=50, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.email

    # def get_absolute_url(self):
    #     return "/users/%i/" % (self.pk)
    
    # def save(self, *args, **kwargs):
    #     # Hash the password if it's set and not hashed already
    #     if self.password and not self.password.startswith("pbkdf2_sha256$"):
    #         self.password = make_password(self.password)
    #     super(User, self).save(*args, **kwargs)





# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
#         free_trial_plan_name = 'Free Trial'
#         # Check if the Free Trial plan exists
#         free_trial_plan, created = SubscriptionPlan.objects.get_or_create(
#             name=free_trial_plan_name,
#             defaults={
#                 'price': 0.00,  # Set the appropriate price for the Free Trial
#                 'features': 'Free Trial Features',
#                 'free_trial': True,
#             }
#         )

#         # If the Free Trial plan didn't exist and was just created, set the start date to now
#         if created:
#             free_trial_plan.start_date = instance.date_joined
#             free_trial_plan.save()

#         Subscription.objects.create(
#             user=instance,
#             plan=free_trial_plan,
#             start_date=instance.date_joined,
#             # end_date=instance.date_joined + timedelta(days=30), 
#             end_date = None
#         )

