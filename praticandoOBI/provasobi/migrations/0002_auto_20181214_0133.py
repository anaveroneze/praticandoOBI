# Generated by Django 2.1 on 2018-12-14 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provasobi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problema',
            name='tituloproblema',
            field=models.TextField(blank=True, db_column='tituloProblema', null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='problema',
            unique_together=set(),
        ),
    ]
