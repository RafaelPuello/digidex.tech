# Generated by Django 5.1 on 2024-10-08 08:27

import django.db.models.deletion
import modelcluster.fields
import uuid
import wagtail.models
import wagtail.search.index
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_basedocument_options_alter_baseimage_options_and_more'),
        ('botany', '0015_remove_plant_date_remove_plant_quantity'),
        ('inventory', '0002_alter_inventoryindexcollection_options'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plantgalleryimage',
            name='plant',
        ),
        migrations.RemoveField(
            model_name='plantgalleryimage',
            name='image',
        ),
        migrations.CreateModel(
            name='UserPlant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('slug', models.SlugField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants', to='inventory.inventoryboxpage')),
                ('locale', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale', verbose_name='locale')),
            ],
            options={
                'verbose_name': 'plant',
                'verbose_name_plural': 'plants',
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model, wagtail.models.PreviewableMixin),
        ),
        migrations.CreateModel(
            name='UserPlantGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='base.baseimage')),
                ('plant', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='botany.userplant')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Plant',
        ),
        migrations.DeleteModel(
            name='PlantGalleryImage',
        ),
        migrations.AddIndex(
            model_name='userplant',
            index=models.Index(fields=['box', 'name'], name='botany_user_box_id_543c5a_idx'),
        ),
        migrations.AddIndex(
            model_name='userplant',
            index=models.Index(fields=['box', 'slug'], name='botany_user_box_id_e14445_idx'),
        ),
        migrations.AddConstraint(
            model_name='userplant',
            constraint=models.UniqueConstraint(fields=('box', 'name'), name='unique_plant_name_in_box'),
        ),
        migrations.AddConstraint(
            model_name='userplant',
            constraint=models.UniqueConstraint(fields=('box', 'slug'), name='unique_plant_slug_in_box'),
        ),
        migrations.AlterUniqueTogether(
            name='userplant',
            unique_together={('translation_key', 'locale')},
        ),
    ]
