# Generated by Django 3.2.23 on 2024-01-03 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20240102_0919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='professor',
            old_name='collegel',
            new_name='college',
        ),
    ]
