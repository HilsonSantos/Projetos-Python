from django.db import models


class Clientes(models.Model):
    CLIENTE_TIPO = (('F', 'Física'), ('J', 'Jurídica'))
    CLIENTE_STATUS = (('A', 'Ativo'), ('I', 'Inativo'))
    cpfcnpj = models.CharField(max_length=19, null=False, blank=False)
    nrazaosocial = models.CharField(max_length=255, null=False, blank=False)
    nfantasia = models.CharField(max_length=150, null=False, blank=False)
    tipo = models.CharField(max_length=1, choices=CLIENTE_TIPO)
    status = models.CharField(max_length=1, choices=CLIENTE_STATUS)

    class META:
        verbose_name_plural = 'Clientes'
        ordering = ['id']

    def __str__(self):
        return self.nrazaosocial
