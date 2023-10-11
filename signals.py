from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Group
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=Group)
def group_pre_save(sender, instance, **kwargs):
    if instance:
        print(f"Group {instance.name} is going to be created")

@receiver(post_save, sender=Group)
def group_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"group {instance.name} is created")
    else:
        print(f"group {instance.name} is not created")

@receiver(pre_delete, sender=Group)
def group_pre_delete(sender, instance, **kwargs):
    if instance:
        print(f"Group {instance.name} is going to be deleted")

@receiver(post_delete, sender = Group)
def group_post_delete(sender, instance, **kwargs):
    print(f"Group {instance.name} is deletd")