# Generated by Django 3.2.23 on 2024-02-06 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_professor_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]