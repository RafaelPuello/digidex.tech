# Generated by Django 5.1 on 2024-09-08 23:23

import django.core.validators
import django.db.models.deletion
import nearfieldcommunication.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NfcTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('serial_number', models.CharField(db_index=True, editable=False, max_length=32, unique=True, validators=[nearfieldcommunication.validators.validate_serial_number])),
                ('integrated_circuit', models.CharField(choices=[('213', 'NTAG 213'), ('215', 'NTAG 215'), ('216', 'NTAG 216')], default='213', max_length=5)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'nfc tag',
                'verbose_name_plural': 'nfc tags',
            },
        ),
        migrations.CreateModel(
            name='NfcTagType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'nfc tag type',
                'verbose_name_plural': 'nfc tag types',
            },
        ),
        migrations.CreateModel(
            name='NfcTagScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('scanned_at', models.DateTimeField(auto_now_add=True)),
                ('nfc_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scans', to='nearfieldcommunication.nfctag')),
            ],
            options={
                'verbose_name': 'nfc tag scan',
                'verbose_name_plural': 'nfc tag scans',
            },
        ),
    ]
