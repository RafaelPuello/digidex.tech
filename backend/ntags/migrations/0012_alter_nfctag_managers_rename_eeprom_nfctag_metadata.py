# Generated by Django 5.1 on 2024-10-17 08:56

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ntags', '0011_alter_nfctag_integrated_circuit'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='nfctag',
            managers=[
                ('tags', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameField(
            model_name='nfctag',
            old_name='eeprom',
            new_name='metadata',
        ),
    ]
