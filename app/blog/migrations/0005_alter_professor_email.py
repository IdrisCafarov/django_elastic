# Generated by Django 3.2.23 on 2024-01-02 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20240102_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
