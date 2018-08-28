# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alternativa(models.Model):
    codalternativa = models.IntegerField(db_column='codAlternativa', primary_key=True)  # Field name made lowercase.
    letraalternativa = models.CharField(db_column='letraAlternativa', max_length=100, blank=True, null=True)  # Field name made lowercase.
    textoalternativa = models.CharField(db_column='textoAlternativa', max_length=100, blank=True, null=True)  # Field name made lowercase.
    codquestao = models.ForeignKey('Questao', models.DO_NOTHING, db_column='codQuestao', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alternativa'


class Prova(models.Model):
    codprova = models.IntegerField(db_column='codProva', primary_key=True)  # Field name made lowercase.
    anoprova = models.IntegerField(db_column='anoProva', blank=True, null=True)  # Field name made lowercase.
    nivelprova = models.IntegerField(db_column='nivelProva', blank=True, null=True)  # Field name made lowercase.
    faseprova = models.IntegerField(db_column='faseProva', blank=True, null=True)  # Field name made lowercase.
    urlprova = models.URLField(db_column='urlProva', null=True, blank=True, default='https://olimpiada.ic.unicamp.br/passadas/')

    class Meta:
        managed = True
        db_table = 'prova'


class Questao(models.Model):
    codquestao = models.IntegerField(db_column='codQuestao', primary_key=True)  # Field name made lowercase.
    numeroquestao = models.IntegerField(db_column='numeroQuestao', blank=True, null=True)  # Field name made lowercase.
    enunciadoquestao = models.CharField(db_column='enunciadoQuestao', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gabaritoquestao = models.CharField(db_column='gabaritoQuestao', max_length=10, blank=True, null=True)
    codprova = models.ForeignKey(Prova, models.DO_NOTHING, db_column='codProva', blank=True, null=True)  # Field name made lowercase.
    codproblema = models.ForeignKey('Problema', models.DO_NOTHING, db_column='codProblema', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'questao'
        db_table = 'questao'

class Problema(models.Model):
    codproblema = models.AutoField(db_column='codProblema', primary_key=True)
    numeroproblema = models.IntegerField(db_column='numeroProblema', blank=True, null=True)
    tituloproblema = models.CharField(db_column='tituloProblema', max_length=100, blank=True, null=True)
    enunciadoproblema = models.CharField(db_column='enunciadoProblema', max_length=500, blank=True, null=True)
    regrasproblema = models.CharField(db_column='regrasProblema', max_length=500, blank=True, null=True)
    imgproblema = models.CharField(db_column='imgProblema', max_length=300, blank=True, null=True, default='')
    codprova = models.ForeignKey('Prova', models.DO_NOTHING, db_column='codProva', blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'problema'

class Classificacao(models.Model):
    codclassificacao = models.AutoField(db_column='codClassificacao', primary_key=True)
    tituloclassificacao = models.CharField(db_column='tituloClassificacao', max_length=100, blank=True, null=True)
    problemas = models.ManyToManyField(Problema)
    class Meta:
        managed = True
        db_table = 'classificacao'