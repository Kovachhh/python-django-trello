from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Board, Column

@receiver(post_save, sender=Board)
def create_default_columns(sender, instance, created, **kwargs):
    if created:
        Column.objects.create(board=instance, name='To Do', color="#FF0000")
        Column.objects.create(board=instance, name='In Progress', color="#FFFF00")
        Column.objects.create(board=instance, name='Done', color="#00FF00")
