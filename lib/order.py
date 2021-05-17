from order.models import *
from decimal import Decimal


class OrderHelper:
    # Calcular rentabilidade do item
    def get_profitability(self, price, product_price):
        minimum_price = product_price - (product_price * Decimal('0.1'))

        if price > product_price:
            return 1
        elif price <= product_price and price >= minimum_price:
            return 0
        elif price < minimum_price:
            return -1

    # Adicionar item
    def item_create(self, order_id, product_id, quantity, price):
        try:
            order = Order.objects.get(pk=order_id)
        except Exception as e:
            raise Exception(e)
            raise Exception('Pedido não encontrado.')

        try:
            product = Product.objects.get(pk=product_id)
        except:
            raise Exception('Produto não encontrado.')

        try:
            item = Item.objects.create(order=order,
                                       product=product,
                                       quantity=quantity,
                                       price=price)
        except:
            raise Exception('Erro ao criar item.')

        return item

    # Remover item
    def item_delete(self, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except:
            raise Exception('Item não encontrado.')

        try:
            item.delete()
        except:
            raise Exception('Erro ao remover item.')

        return True
