# Generated by Django 5.1 on 2024-10-01 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botany', '0009_alter_plantgalleryimage_image'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='plant',
            index=models.Index(fields=['box', 'slug'], name='botany_plan_box_id_0387f8_idx'),
        ),
        migrations.AddConstraint(
            model_name='plant',
            constraint=models.UniqueConstraint(fields=('box', 'slug'), name='unique_plant_slug_in_box'),
        ),
    ]
