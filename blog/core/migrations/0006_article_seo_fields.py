from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_subscriber_alter_article_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='seo_meta_title',
            field=models.CharField(
                blank=True,
                help_text='Title used in the browser tab and search results (recommended: 50-60 characters).',
                max_length=70,
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='seo_meta_description',
            field=models.CharField(
                blank=True,
                help_text='Short summary shown in search results (recommended: 150-160 characters).',
                max_length=160,
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='seo_meta_keywords',
            field=models.CharField(
                blank=True,
                help_text='Comma-separated keywords relevant to this article.',
                max_length=255,
            ),
        ),
    ]
