# models.py
from django.db import models

class Posto(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Tanque(models.Model):
    TIPOS_COMBUSTIVEL = [
        ('GASOLINA', 'Gasolina'),
        ('DIESEL', 'Óleo Diesel')
    ]
    
    tipo_combustivel = models.CharField(max_length=10, choices=TIPOS_COMBUSTIVEL)
    capacidade = models.FloatField()
    nivel_atual = models.FloatField()
    posto = models.ForeignKey(Posto, related_name='tanques', on_delete=models.CASCADE)

    def criar_nivel_atual(self):
        self.nivel_atual = self.capacidade
    
    def save(self, *args, **kwargs):
        self.criar_nivel_atual()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_tipo_combustivel_display()} - Capacidade: {self.capacidade}L - Posto: {self.posto.nome}'


class Bomba(models.Model):
    identificacao = models.CharField(max_length=250)
    tanque = models.ForeignKey(Tanque, related_name='bombas', on_delete=models.CASCADE)

    def __str__(self):
        return f'Bomba {self.identificacao} - Tanque {self.tanque.tipo_combustivel} - Posto: {self.tanque.posto.nome}'


class PrecoCombustivel(models.Model):
    TIPOS_COMBUSTIVEL = [
        ('GASOLINA', 'Gasolina'),
        ('DIESEL', 'Óleo Diesel')
    ]
    
    tipo_combustivel = models.CharField(max_length=10, choices=TIPOS_COMBUSTIVEL)
    preco_por_litro = models.FloatField()
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.get_tipo_combustivel_display()} - R$ {self.preco_por_litro} - Atualizado em {self.data_atualizacao}'


class Abastecimento(models.Model):
    bomba = models.ForeignKey(Bomba, related_name='abastecimentos', on_delete=models.CASCADE)
    litros = models.FloatField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    imposto = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            preco_combustivel = PrecoCombustivel.objects.filter(
                tipo_combustivel=self.bomba.tanque.tipo_combustivel
            ).latest('data_atualizacao')
            self.valor = self.litros * preco_combustivel.preco_por_litro
            self.imposto = self.valor * 0.13
            self.bomba.tanque.nivel_atual -= self.litros
            self.bomba.tanque.save()
        super().save(*args, **kwargs)

    def data_formatada(self):
        return self.data.strftime('%d/%m/%Y %H:%M')

    def __str__(self):
        return f'Abastecimento {self.id} - Bomba - {self.bomba.identificacao} - Posto: {self.bomba.tanque.posto.nome}'
