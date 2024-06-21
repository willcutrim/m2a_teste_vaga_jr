import io
from PyPDF2 import PdfWriter, PdfReader
from django.forms import BaseModelForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from datetime import datetime, timedelta
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView
from .models import Abastecimento, Bomba, Tanque, PrecoCombustivel, Posto
from .forms import AbastecimentoForm, PostoForm, PrecoCombustivelForm, BombaForm, TanqueForm
from .utils import gerar_relatorio
from django.http import HttpResponse
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect




class CriarAbastecimentoView(CreateView):

    model = Abastecimento
    form_class = AbastecimentoForm
    template_name = 'html/criar_abastecimento.html'
    success_url = reverse_lazy('relatorio_abastecimentos')

    def form_valid(self, form):
        bomba = form.cleaned_data['bomba']
        litros = form.cleaned_data['litros']
        tipo_combustivel = bomba.tanque.tipo_combustivel
        
        try:
            preco_combustivel = PrecoCombustivel.objects.filter(tipo_combustivel=tipo_combustivel).latest('data_atualizacao')
        except PrecoCombustivel.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, f'Não há preço cadastrado para o combustível {tipo_combustivel}. Por favor, cadastre o preço primeiro.')
            form.add_error(None, f'Não há preço cadastrado para o combustível {tipo_combustivel}. Por favor, cadastre o preço primeiro.')
            return self.form_invalid(form)

        capacidade_tanque = bomba.tanque.capacidade
        nivel_atual = bomba.tanque.nivel_atual
        if litros > nivel_atual:

            form.add_error('litros', f'O abastecimento ultrapassa a capacidade máxima do tanque ({capacidade_tanque} litros. Nível atual: {nivel_atual} litros).')
            return self.render_to_response(self.get_context_data(form=form))
    
        tanque = Tanque.objects.filter(id=bomba.tanque.id).first()
        tanque.nivel_atual -= litros
        tanque.save()
        
        return super().form_valid(form)


class CriarBombaView(CreateView):

    model = Bomba
    form_class = BombaForm
    template_name = 'html/criar_bomba.html'
    success_url = reverse_lazy('criar_bomba')

class CriarTanqueView(CreateView):

    model = Tanque
    form_class = TanqueForm
    template_name = 'html/criar_tanque.html'
    success_url = reverse_lazy('criar_tanque')

class CriarPostoView(CreateView):

    model = Posto
    form_class = PostoForm
    template_name = 'html/criar_posto.html'
    success_url = reverse_lazy('criar_posto')


class CriarPrecoCombustivelView(CreateView):

    model = PrecoCombustivel
    form_class = PrecoCombustivelForm
    template_name = 'html/criar_preco_combustivel.html'
    success_url = reverse_lazy('criar_preco_combustivel')

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
        p.drawString(170, y, f"Tanque: {abastecimento.bomba.tanque.tipo_combustivel}")
        p.drawString(290, y, f"Bomba: {abastecimento.bomba.identificacao}")
        p.drawString(450, y, f"Valor: R$ {abastecimento.valor}")
        y -= 20

        total_litros += abastecimento.litros
        total_valor += abastecimento.valor
        total_imposto += abastecimento.imposto
    
    altura_pagina = 800

    y = 50
    p.drawString(400, y, f"Total de Imposto: R${total_imposto}")
    p.drawString(250, y, f"Valor total: R${total_valor}")
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

