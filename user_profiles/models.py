from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    def_user = models.OneToOneField(User, on_delete=models.CASCADE)
    def_street = models.CharField(max_length=100, null=True, blank=True)
    def_town = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

@reciever(post_save, sender=User)
def create_update_profile(sender,instance, created, **kwargs):
    """
    Create/Update profile
    """
    if created:
        Profile.objects.create(user=instance)

    instance.userprofile.save()