from celery import shared_task
from .models import Card
from django.utils import timezone

@shared_task
def update_card_status():
    """
    Crontab function to check expired cards
    """
    cards = Card.objects.filter(status='Active', expire_date__lt=timezone.now())
    cards.update(status='Expired')