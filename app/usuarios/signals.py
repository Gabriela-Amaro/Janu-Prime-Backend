from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

import logging

logger = logging.getLogger("app")

Usuario = get_user_model()

@receiver(pre_delete, sender=Usuario)
def blacklist_tokens_on_user_delete(sender, instance, **kwargs):
    for outstanding_token in OutstandingToken.objects.filter(user=instance):
        BlacklistedToken.objects.get_or_create(token=outstanding_token)

    logger.info(
        "Tokens para o usuário %s foram adicionados à blacklist.",
        instance.email,
    )