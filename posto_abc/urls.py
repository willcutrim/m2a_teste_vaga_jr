from django.urls import path
from .views import (CriarAbastecimentoView, 
                    RelatorioAbastecimentosView, AbastecimentosBombaView, 
                    gerar_pdf_abastecimentos, CriarBombaView, CriarPostoView, 
                    CriarTanqueView, CriarPrecoCombustivelView)

urlpatterns = [
    path('criar_abastecimento/', CriarAbastecimentoView.as_view(), name='criar_abastecimento'),
    path('', RelatorioAbastecimentosView.as_view(), name='relatorio_abastecimentos'),
    path('abastecimentos_bomba/<int:pk>/<str:data>/', AbastecimentosBombaView.as_view(), name='abastecimentos_bomba'),
    path('gerar_pdf_abastecimentos/<int:bomba_id>/<str:data>/', gerar_pdf_abastecimentos, name='gerar_pdf_abastecimentos'),


    path('criar_bomba/', CriarBombaView.as_view(), name='criar_bomba'),
    path('criar_posto/', CriarPostoView.as_view(), name='criar_posto'),
    path('criar_tanque/', CriarTanqueView.as_view(), name='criar_tanque'),
    path('criar_preco_combustivel/', CriarPrecoCombustivelView.as_view(), name='criar_preco_combustivel'),
]
    