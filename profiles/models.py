from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def_first_name = models.CharField(max_length=50, null=True, blank=True)
    def_last_name = models.CharField(max_length=50, null=True, blank=True)
    def_email = models.EmailField(max_length=50, null=True, blank=True)
    def_phone = models.CharField(max_length=50, null=True, blank=True)
    def_street = models.CharField(max_length=100, null=True, blank=True)
    def_town = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)

    instance.userprofile.save()
