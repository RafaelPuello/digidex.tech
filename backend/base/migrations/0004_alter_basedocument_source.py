# Generated by Django 5.1 on 2024-09-21 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_basedocument_options_alter_baseimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basedocument',
            name='source',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
