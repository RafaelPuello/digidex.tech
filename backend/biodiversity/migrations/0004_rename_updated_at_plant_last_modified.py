# Generated by Django 5.1 on 2024-09-17 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biodiversity', '0003_remove_plant_nfc_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plant',
            old_name='updated_at',
            new_name='last_modified',
        ),
    ]
