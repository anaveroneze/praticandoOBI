# Generated by Django 2.1 on 2018-09-25 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provasobi', '0012_auto_20180922_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='provaperson',
            name='questoes',
            field=models.ManyToManyField(blank='True', to='provasobi.Questao'),
        ),
    ]
