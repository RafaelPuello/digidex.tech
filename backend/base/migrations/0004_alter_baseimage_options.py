# Generated by Django 5.1 on 2024-10-18 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_instagtram_url_navigationsettings_instagram_url_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseimage',
            options={'verbose_name': 'image', 'verbose_name_plural': 'images'},
        ),
    ]
