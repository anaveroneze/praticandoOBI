# Generated by Django 2.1 on 2018-09-22 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
	('ook', '__first__'),
        ('usuarios', '0007_auto_20180922_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='localizacao',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
