# urls.py
from django.urls import path
from .views import (CriarAbastecimentoView, 
                    RelatorioAbastecimentosView, AbastecimentosBombaView, 
                    gerar_pdf_abastecimentos)

urlpatterns = [
    path('criar_abastecimento/', CriarAbastecimentoView.as_view(), name='criar_abastecimento'),
    path('', RelatorioAbastecimentosView.as_view(), name='relatorio_abastecimentos'),
    path('abastecimentos_bomba/<int:pk>/<str:data>/', AbastecimentosBombaView.as_view(), name='abastecimentos_bomba'),
    path('gerar_pdf_abastecimentos/<int:bomba_id>/<str:data>/', gerar_pdf_abastecimentos, name='gerar_pdf_abastecimentos'),
]
    