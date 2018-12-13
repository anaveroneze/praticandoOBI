# Generated by Django 2.1 on 2018-12-01 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('localizacao', models.CharField(blank=True, default='', max_length=100)),
                ('instituicao', models.CharField(blank=True, default='', max_length=100)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
            ],
        ),
    ]