import asyncio

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NewsLetter, User
import requests
from dj_config import BOT_TOKEN


@receiver(post_save, sender=NewsLetter)
async def on_faq_save(sender, instance: NewsLetter, created, **kwargs):
    if created:
        async for user in User.objects.all():
            payload = {
                'chat_id': user.id,
                'text': instance.letter,
                'parse_mode': 'HTML'
            }
            requests.post(
                url=f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                json=payload,
            )
            await asyncio.sleep(0.1)
