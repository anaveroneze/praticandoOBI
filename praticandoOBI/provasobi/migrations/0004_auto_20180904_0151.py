# Generated by Django 2.1 on 2018-09-04 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provasobi', '0003_provaperson'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provaperson',
            old_name='author',
            new_name='autor',
        ),
    ]
