# Generated by Django 5.1 on 2024-10-05 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ntags', '0011_remove_nfctagtype_collection_alter_nfctag_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nfctag',
            name='nfc_tag_type',
        ),
        migrations.DeleteModel(
            name='NFCTagType',
        ),
    ]
