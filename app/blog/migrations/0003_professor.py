# Generated by Django 3.2.23 on 2024-01-02 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('research_areas', models.TextField(blank=True, null=True)),
                ('university', models.CharField(max_length=1000)),
                ('department', models.CharField(max_length=1000)),
            ],
        ),
    ]
