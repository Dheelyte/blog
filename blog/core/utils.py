import os


def article_thumbnail_path(instance, filename):
    """Generate path for article thumbnails: articles/thumbnails/{slug}"""
    return os.path.join('articles', 'thumbnails', str(instance.slug))