# Generated by Django 3.2.23 on 2024-01-02 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=120, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='User Name')),
                ('surname', models.CharField(blank=True, max_length=40, null=True, verbose_name='User Surname')),
                ('profil_image', models.ImageField(blank=True, null=True, upload_to='Profile Image')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_disable', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'MyUser',
                'verbose_name_plural': 'MyUser',
                'ordering': ['-timestamp'],
            },
        ),
    ]
