from django.contrib import admin
from .models import Tanque, Bomba, Abastecimento, Posto, PrecoCombustivel

@admin.register(Posto)
class PostoAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Tanque)
class TanqueAdmin(admin.ModelAdmin):
    list_display = ('tipo_combustivel', 'capacidade', 'nivel_atual', 'posto')


@admin.register(Bomba)
class BombaAdmin(admin.ModelAdmin):
    list_display = ('identificacao', 'tanque', 'tanque__posto')

    def tanque__posto(self, obj):
        return obj.tanque.posto.nome
    tanque__posto.short_description = 'Posto'


@admin.register(Abastecimento)
class AbastecimentoAdmin(admin.ModelAdmin):
    list_display = ('bomba', 'litros', 'valor', 'imposto', 'data', 'bomba__tanque__posto')

    def bomba__tanque__posto(self, obj):
        return obj.bomba.tanque.posto.nome
    bomba__tanque__posto.short_description = 'Posto'


@admin.register(PrecoCombustivel)
class PrecoCombustivelAdmin(admin.ModelAdmin):
    list_display = ('tipo_combustivel', 'preco_por_litro', 'data_atualizacao')
