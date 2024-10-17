# Generated by Django 5.1 on 2024-10-17 18:19

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('botany', '0007_alter_userplant_box'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplant',
            name='notes',
            field=wagtail.fields.StreamField([('heading', 2), ('image', 8), ('body', 9)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'form_classname': 'title', 'required': True}), 1: ('wagtail.blocks.ChoiceBlock', [], {'blank': True, 'choices': [('', 'Select a heading size'), ('h2', 'H2'), ('h3', 'H3')], 'required': False}), 2: ('wagtail.blocks.StructBlock', [[('heading_value', 0), ('size', 1)]], {'required': False}), 3: ('wagtail.blocks.BooleanBlock', (), {'required': False}), 6: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': True}), 7: ('wagtail.blocks.CharBlock', (), {'required': False}), 8: ('wagtail.blocks.StructBlock', [[('image', 6), ('caption', 7), ('attribution', 7)]], {'required': False}), 9: ('base.blocks.BaseBodyBlock', (), {})}),
        ),
    ]
