from django.core.management.base import BaseCommand
from produtos.models import Produto 
from constance import config 

class Command(BaseCommand):
    help = 'Recalcula os pontos de todos os produtos com base na constante de cashback atual.'

    def handle(self, *args, **options):
        if config.PORCENTAGEM_CASHBACK <= 0:
            self.stdout.write(self.style.ERROR('A PORCENTAGEM_CASHBACK não está configurada ou é zero.'))
            return

        self.stdout.write('Iniciando recálculo de pontos...')
        
        produtos = Produto.objects.all()
        count = 0
        
        for produto in produtos:
            produto.save() # recalcula e salva os pontos
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'{count} produtos foram atualizados com sucesso.'))