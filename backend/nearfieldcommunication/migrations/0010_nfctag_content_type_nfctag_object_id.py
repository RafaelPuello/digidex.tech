# Generated by Django 5.1 on 2024-09-17 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nearfieldcommunication', '0009_nfctagmemory'),
    ]

    operations = [
        migrations.AddField(
            model_name='nfctag',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='nfctag',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
