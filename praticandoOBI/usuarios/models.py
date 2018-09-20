from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from provasobi.models import ProvaPerson

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    localizacao = models.CharField(max_length=30, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    provas = models.ManyToManyField(ProvaPerson, blank=True)

    def __str__(self):
        return self.user.username + ' ' + self.localizacao

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
