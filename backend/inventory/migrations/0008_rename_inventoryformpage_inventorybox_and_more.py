# Generated by Django 5.1 on 2024-10-21 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botany', '0016_remove_userplant_notes_userplant_image_plantnote_and_more'),
        ('inventory', '0007_inventoryformsubmission'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InventoryFormPage',
            new_name='InventoryBox',
        ),
        migrations.RenameModel(
            old_name='InventoryIndexPage',
            new_name='InventoryIndex',
        ),
    ]
