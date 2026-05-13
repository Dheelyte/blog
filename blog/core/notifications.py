from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, get_connection

from .models import Article, Subscriber


def send_new_article_emails(article_id):
    try:
        article = Article.objects.select_related('author').get(pk=article_id)
    except Article.DoesNotExist:
        return

    recipients = list(
        Subscriber.objects.filter(confirmed=True).values_list('email', flat=True)
    )
    if not recipients:
        return

    try:
        domain = Site.objects.get_current().domain
    except Exception:
        domain = 'harribenhub.com'

    scheme = 'https'
    article_url = f"{scheme}://{domain}{article.get_absolute_url()}"
    unsubscribe_hint = f"{scheme}://{domain}/"

    subject = f"New post: {article.title}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@harribenhub.com')

    text_body = (
        f"Hi,\n\n"
        f"A new article has just been published on Harriben Hub:\n\n"
        f"{article.title}\n"
        f"{article_url}\n\n"
        f"Read it here: {article_url}\n\n"
        f"— Harriben Hub\n"
        f"You're receiving this because you subscribed to our newsletter at {unsubscribe_hint}\n"
    )

    html_body = (
        f"<p>Hi,</p>"
        f"<p>A new article has just been published on <strong>Harriben Hub</strong>:</p>"
        f"<h2 style=\"margin:1rem 0;\"><a href=\"{article_url}\">{article.title}</a></h2>"
        f"<p><a href=\"{article_url}\" "
        f"style=\"display:inline-block;padding:10px 18px;background:#111;color:#fff;"
        f"text-decoration:none;border-radius:6px;\">Read the article</a></p>"
        f"<p style=\"color:#666;font-size:12px;margin-top:2rem;\">"
        f"You're receiving this because you subscribed to the Harriben Hub newsletter."
        f"</p>"
    )

    connection = get_connection()
    messages = []
    for email in recipients:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=[email],
            connection=connection,
        )
        msg.attach_alternative(html_body, "text/html")
        messages.append(msg)

    try:
        connection.send_messages(messages)
        print("Post notifications sent")
    except Exception:
        pass
