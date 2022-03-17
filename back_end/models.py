from django.db import models
from django.core.validators import RegexValidator


class BlastJob(models.Model):
    dna_validator = RegexValidator('^[CAGTcagt]+$','This value may contain only a DNA sequence (CAGT - not case sensitive)')
    query = models.CharField(max_length=255, blank=False, null=True, validators=[dna_validator])

    #Uncomment to disable regexValidator
    #query = models.CharField(max_length=255, blank=False, null=True)

class BlastResult(models.Model):
    blast_job = models.ForeignKey(BlastJob, blank=False, null=False, on_delete=models.CASCADE)
    result_no = models.IntegerField(blank=False, null=False ,default=0)
    sstart = models.IntegerField(blank=False, null=False)
    send = models.IntegerField(blank=False, null=False)
    sstrand = models.CharField(max_length=5)
    evalue = models.FloatField(blank=False, null=False)
    pident = models.FloatField(blank=False, null=False)
    sequence = models.CharField(max_length=255, blank=False, null=False)
