import threading

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Article


@receiver(pre_save, sender=Article)
def _stash_previous_publish_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            prev = Article.objects.only('published_at').get(pk=instance.pk)
            instance._was_published = prev.published_at is not None
        except Article.DoesNotExist:
            instance._was_published = False
    else:
        instance._was_published = False


@receiver(post_save, sender=Article)
def _notify_subscribers_on_first_publish(sender, instance, **kwargs):
    if getattr(instance, '_was_published', False):
        return
    if not instance.is_published:
        return
    if getattr(instance, '_notification_dispatched', False):
        return
    instance._notification_dispatched = True

    from .notifications import send_new_article_emails
    threading.Thread(
        target=send_new_article_emails,
        args=(instance.pk,),
        daemon=True,
    ).start()
