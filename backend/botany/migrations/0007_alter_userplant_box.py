# Generated by Django 5.1 on 2024-10-16 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botany', '0006_remove_userplant_unique_plant_name_user_and_more'),
        ('inventory', '0004_alter_inventoryindexpage_user_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userplant',
            name='box',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants', to='inventory.inventoryboxpage'),
        ),
    ]
