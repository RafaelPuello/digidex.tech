# Generated by Django 5.1 on 2024-10-15 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botany', '0003_remove_userplant_unique_plant_name_in_box_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userplant',
            name='unique_plant_slug_user',
        ),
        migrations.RemoveIndex(
            model_name='userplant',
            name='botany_user_user_id_b9e319_idx',
        ),
        migrations.RemoveField(
            model_name='userplant',
            name='slug',
        ),
    ]
