from django.db import migrations

def migrate_nfctags(apps, schema_editor):
    OldNfcTag = apps.get_model('inventory', 'NearfieldcommunicationTag')
    NewNfcTag = apps.get_model('nearfieldcommunication', 'NfcTag')

    # Copy data from the old table to the new one
    for old_tag in OldNfcTag.objects.all():
        NewNfcTag.objects.create(
            uuid=old_tag.uuid,
            serial_number=old_tag.serial_number,
            owner=old_tag.owner,
            label=old_tag.label,
            type=old_tag.type,
            active=old_tag.active,
            created_at=old_tag.created_at,
            last_modified=old_tag.last_modified,
        )

class Migration(migrations.Migration):

    dependencies = [
        ('nearfieldcommunication', '0002_remove_nfcrecord_asset_nfcrecord_content_type_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_nfctags),
    ]
