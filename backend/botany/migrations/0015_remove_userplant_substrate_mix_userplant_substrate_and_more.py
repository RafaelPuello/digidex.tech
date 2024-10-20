# Generated by Django 5.1 on 2024-10-20 06:40

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botany', '0014_alter_userplant_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userplant',
            name='substrate_mix',
        ),
        migrations.AddField(
            model_name='userplant',
            name='substrate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='botany.substratemix'),
        ),
        migrations.AddField(
            model_name='userplant',
            name='taxon_id',
            field=models.PositiveBigIntegerField(blank=True, default=6),
        ),
        migrations.AlterField(
            model_name='userplant',
            name='notes',
            field=wagtail.fields.StreamField([('note', 3)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'form_classname': 'title'}), 1: ('wagtail.blocks.DateBlock', (), {}), 2: ('wagtail.blocks.TextBlock', (), {}), 3: ('wagtail.blocks.StructBlock', [[('heading', 0), ('date', 1), ('body', 2)]], {})}),
        ),
    ]
