# Generated by Django 5.1 on 2024-09-07 23:22

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('trainer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user inventory',
                'verbose_name_plural': 'user inventories',
            },
        ),
        migrations.DeleteModel(
            name='UserInventory',
        ),
        migrations.AddIndex(
            model_name='trainerinventory',
            index=models.Index(fields=['uuid'], name='inventory_t_uuid_74c307_idx'),
        ),
    ]
