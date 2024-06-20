import io
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from datetime import datetime, timedelta
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView
from .models import Abastecimento, Bomba
from .forms import AbastecimentoForm
from .utils import gerar_relatorio
from django.http import HttpResponse

from django.shortcuts import get_object_or_404




class CriarAbastecimentoView(CreateView):
    model = Abastecimento
    form_class = AbastecimentoForm
    template_name = 'html/criar_abastecimento.html'
    success_url = reverse_lazy('relatorio_abastecimentos')



class RelatorioAbastecimentosView(TemplateView):
    template_name = 'html/relatorio_abastecimentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_inicio = self.request.GET.get('data_inicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        data_fim = self.request.GET.get('data_fim', datetime.now().strftime('%Y-%m-%d'))
        
        relatorio = gerar_relatorio(data_inicio, data_fim)
        total_valor, total_imposto = self.calcular_totais(relatorio)
        
        context.update({
            'relatorio': relatorio,
            'total_valor': total_valor,
            'total_imposto': total_imposto,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
        })
        return context

    def calcular_totais(self, relatorio):
        total_valor = relatorio.aggregate(total_valor=Sum('total_valor'))['total_valor']
        total_imposto = relatorio.aggregate(total_imposto=Sum('total_imposto'))['total_imposto']
        return total_valor, total_imposto



class AbastecimentosBombaView(DetailView):
    model = Bomba
    template_name = 'html/abastecimentos.html'
    context_object_name = 'bomba'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.kwargs.get('data')
        data_formatada = datetime.strptime(data, '%Y-%m-%d').date()
        
        abastecimentos = Abastecimento.objects.filter(bomba=self.object, data__date=data_formatada)
        
        context.update({
            'abastecimentos': abastecimentos,
            'data': data_formatada,
        })
        return context



class HomeView(TemplateView):
    template_name = 'html/home.html'





def gerar_pdf_abastecimentos(request, bomba_id, data):

    bomba = get_object_or_404(Bomba, id=bomba_id)
    data_formatada = datetime.strptime(data, '%Y-%m-%d').date()
    abastecimentos = Abastecimento.objects.filter(bomba=bomba, data__date=data_formatada)

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 780, f"Relatório de Abastecimentos da Bomba {bomba.identificacao} em {data_formatada}")

    p.setFont("Helvetica", 10)

    p.drawString(120, 770, "-" * 90)
    
    y = 750
    total_litros = 0
    total_valor = 0
    total_imposto = 0

    for abastecimento in abastecimentos:
        p.drawString(50, y, f"Data: {abastecimento.data_formatada()}")
        p.drawString(200, y, f"Litros: {abastecimento.litros}")
        p.drawString(300, y, f"Valor: R${abastecimento.valor}")
        p.drawString(400, y, f"Imposto: R${abastecimento.imposto}")
        y -= 20

        total_litros += abastecimento.litros
        total_valor += abastecimento.valor
        total_imposto += abastecimento.imposto
    
    altura_pagina = 800

    y = 50
    p.drawString(400, y, f"Total de Imposto: R${total_imposto}")
    p.drawString(200, y, f"Valor total: R${total_valor}")
    p.drawString(50, y, f"Total de Litros: {total_litros}")

    p.save()

    buffer.seek(0)

    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(buffer)
    pdf_writer.add_page(pdf_reader.pages[0])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_abastecimentos_{bomba.identificacao}_{data_formatada}.pdf"'

    pdf_writer.write(response)

    return response

