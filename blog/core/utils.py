import os


def article_thumbnail_path(instance, filename):
    """Generate path for article thumbnails: articles/thumbnails/{slug}"""
    return os.path.join('articles', 'thumbnails', str(instance.slug))


def get_user_ip_address(request):

    remote_addr = request.META.get("HTTP_X_FORWARDED_FOR")

    if remote_addr:
        address = remote_addr.split(",")[-1].strip()
    else:
        address = request.META.get("REMOTE_ADDR")

    return address
