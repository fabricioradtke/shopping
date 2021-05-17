from django.core.management.base import BaseCommand
from datetime import datetime
from decimal import Decimal
import sys

from order.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--- iniciando script ---')
        now = datetime.now()

        try:
            self.go(options)
        except KeyboardInterrupt:
            sys.exit()

        print('tempo de execucao: %s' % (datetime.now() - now))
        print('--- script finalizado com sucesso ---')

    def go(self, options):
        # Insert clients data
        try:
            Client.objects.bulk_create([
                Client(name='Darth​ ​Vader'),
                Client(name='Obi-Wan​ ​Kenobi'),
                Client(name='Luke​ ​Skywalker'),
                Client(name='Imperador​ ​Palpatine'),
                Client(name='Han​ ​Solo')
            ])
        except Exception as e:
            print(f'erro ao importar clientes: {e}')
            return

        print('Clientes importados com sucesso')

        # Insert products data
        try:
            Product.objects.bulk_create([
                Product(name='Millenium​ ​Falcon',           price=Decimal('550000.00')),
                Product(name='X-Wing',                     price=Decimal('60000.00'), multiple=2),
                Product(name='Super​ ​Star​ ​Destroyer',       price=Decimal('4570000.00')),
                Product(name='TIE​ ​Fighter',                price=Decimal('75000.00'), multiple=2),
                Product(name='Lightsaber',                 price=Decimal('6000.00'),  multiple=5),
                Product(name='DLT-19​ ​Heavy​ ​Blaster​ ​Rifle', price=Decimal('5800.00')),
                Product(name='DL-44​ ​Heavy​ ​Blaster​ ​Pistol', price=Decimal('1500.00'),  multiple=10)
            ])
        except Exception as e:
            print(f'erro ao importar produtos: {e}')
            return

        print('Produtos importados com sucesso')
