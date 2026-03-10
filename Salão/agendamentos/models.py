from django.db import models
from django.utils import timezone
from django_softdelete.models import SoftDeleteModel

class Cliente(SoftDeleteModel):
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Servico(SoftDeleteModel):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome


class Profissional(SoftDeleteModel):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Agendamento(SoftDeleteModel):

    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'data_hora']),
        ]

    def __str__(self):
        return f"{self.cliente} - {self.servico}"

    @classmethod
    def atualizar_statuss(cls):
        cls.objects.filter(status='AGENDADO', data_hora__lte=timezone.now()).update(status='CONCLUIDO')

    def clean(self):
        from django.core.exceptions import ValidationError
        
        agendamentos_existentes = Agendamento.objects.filter(
            data_hora=self.data_hora,
            status__in=['AGENDADO', 'CONCLUIDO']
        )
        
        if self.pk:
            agendamentos_existentes = agendamentos_existentes.exclude(pk=self.pk)
        
        if agendamentos_existentes.exists():
            raise ValidationError({'data_hora': 'Já existe um agendamento agendado para este horário.'})

    def save(self, *args, **kwargs):
        self.full_clean()  #executa as validações do clean()
        if self.data_hora and self.data_hora <= timezone.now() and self.status == 'AGENDADO':
            self.status = 'CONCLUIDO'
        super().save(*args, **kwargs)
