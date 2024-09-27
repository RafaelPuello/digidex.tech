# Generated by Django 5.1 on 2024-09-27 00:46

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', models.TextField(blank=True)),
                ('body', wagtail.fields.RichTextField(blank=True)),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.collection')),
            ],
            options={
                'verbose_name': 'company index page',
                'verbose_name_plural': 'company index pages',
            },
            bases=('wagtailcore.page',),
        ),
    ]
