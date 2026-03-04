from django.shortcuts import render
from django.db.models import Count
from django.utils.dateparse import parse_date
from .models import Agendamento

def relatorio_servicos(request):
    data_inicio = request.GET.get('inicio')
    data_fim = request.GET.get('fim')

    agendamentos = Agendamento.objects.filter(status='CONCLUIDO')

    if data_inicio and data_fim:
        agendamentos = agendamentos.filter(
            data_horadaterange=[data_inicio, data_fim]
        )

    total = agendamentos.aggregate(total=Count('id'))['total']

    context = {
        'total': total,
        'inicio': data_inicio,
        'fim': data_fim,
    }

    return render(request, 'relatorio.html', context)