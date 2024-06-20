from .models import Abastecimento
from django.db.models import Sum

def gerar_relatorio(data_inicio, data_fim):
    if not data_inicio or not data_fim:
        abastecimentos = Abastecimento.objects.all()
    else:
        abastecimentos = Abastecimento.objects.filter(data__date__range=[data_inicio, data_fim])

    relatorio = abastecimentos.values(
        'data__date', 
        'bomba__tanque__tipo_combustivel', 
        'bomba__identificacao', 
        'bomba__tanque__posto__nome',
        'bomba_id'
    ).annotate(
        total_valor=Sum('valor'),
        total_imposto=Sum('imposto'),
        total_litros=Sum('litros')
    ).order_by('data__date', 'bomba__tanque__tipo_combustivel', 'bomba__identificacao')

    return relatorio




def calcular_valor_total_abastecido(abastecimentos):
    return abastecimentos.aggregate(Sum('valor'))