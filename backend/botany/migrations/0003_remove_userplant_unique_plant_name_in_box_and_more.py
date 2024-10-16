# Generated by Django 5.1 on 2024-10-15 19:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botany', '0002_initial'),
        ('wagtailcore', '0094_alter_page_locale'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userplant',
            name='unique_plant_name_in_box',
        ),
        migrations.RemoveConstraint(
            model_name='userplant',
            name='unique_plant_slug_in_box',
        ),
        migrations.RemoveIndex(
            model_name='userplant',
            name='botany_user_box_id_543c5a_idx',
        ),
        migrations.RemoveIndex(
            model_name='userplant',
            name='botany_user_box_id_e14445_idx',
        ),
        migrations.RemoveField(
            model_name='userplant',
            name='box',
        ),
        migrations.RemoveField(
            model_name='userplant',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='userplant',
            name='last_modified',
        ),
        migrations.AddField(
            model_name='userplant',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plants', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name='userplant',
            index=models.Index(fields=['user', 'name'], name='botany_user_user_id_44496c_idx'),
        ),
        migrations.AddIndex(
            model_name='userplant',
            index=models.Index(fields=['user', 'slug'], name='botany_user_user_id_b9e319_idx'),
        ),
        migrations.AddConstraint(
            model_name='userplant',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_plant_name_user'),
        ),
        migrations.AddConstraint(
            model_name='userplant',
            constraint=models.UniqueConstraint(fields=('user', 'slug'), name='unique_plant_slug_user'),
        ),
    ]
