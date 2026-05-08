from django.db.models import Count, Q

from .models import Category


def categories(request):
    """Expose categories that have at least one published article.

    This is used in the global navigation and footer so we never advertise
    an empty category to readers (or to ad-network reviewers).
    """
    qs = (
        Category.objects
        .annotate(
            published_count=Count('articles', filter=Q(articles__published=True))
        )
        .filter(published_count__gt=0)
        .order_by('name')
    )
    return {'categories': qs}
