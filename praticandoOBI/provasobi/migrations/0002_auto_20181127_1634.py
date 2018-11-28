# Generated by Django 2.1 on 2018-11-27 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('provasobi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='provaperson',
            name='autor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='usuarios.Profile'),
        ),
        migrations.AddField(
            model_name='provaperson',
            name='questoes',
            field=models.ManyToManyField(blank='True', to='provasobi.Questao'),
        ),
        migrations.AddField(
            model_name='problema',
            name='classificacao',
            field=models.ManyToManyField(blank=True, to='provasobi.Classificacao'),
        ),
        migrations.AddField(
            model_name='problema',
            name='codprova',
            field=models.ForeignKey(blank=True, db_column='codProva', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='provasobi.Prova'),
        ),
        migrations.AddField(
            model_name='alternativa',
            name='codquestao',
            field=models.ForeignKey(blank=True, db_column='codQuestao', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='provasobi.Questao'),
        ),
    ]