from django.db import models

class Rios(models.Model):
    
    RISCO_CHOICES = [
        (1, 'Baixo'),
        (2, 'Médio'),
        (3, 'Alto'),
        (4, 'Muito Alto'),
    ]
    
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    risco_inundacao = models.IntegerField(choices=RISCO_CHOICES)

    def __str__(self):
        return self.nome