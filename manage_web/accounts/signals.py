from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Reviewer

@receiver(post_save, sender=User)
def create_reviewer(sender, instance, created, **kwargs):
    if created:
        Reviewer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_reviewer(sender, instance, **kwargs):
    instance.reviewer.save()
        