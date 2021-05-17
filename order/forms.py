from django import forms
from order.models import *
from order.widgets import CustomSelect

from lib.order import OrderHelper


class OrderForm(forms.Form):
    client = forms.ModelChoiceField(label='Cliente', 
                                    empty_label='Selecione', 
                                    queryset=Client.objects.all())


class ItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        products = Product.objects.all()

        choices = list(products.values_list('id', 'name'))
        choices.insert(0, ('', 'Selecione'))

        data = {'data-price': dict(products.values_list('id', 'price'))}
        data['data-price'][''] = ''

        self.fields['product_id'].choices = choices
        self.fields['product_id'].widget = CustomSelect(choices=choices, data=data)

    product_id = forms.ChoiceField(label='Produto')

    quantity = forms.IntegerField(label='Quantidade',
                                  min_value=1,
                                  initial=1)

    price = forms.DecimalField(label='Preço (R$)',
                               max_digits=10,
                               decimal_places=2,
                               min_value=0,
                               initial=0,
                               localize=True,
                               widget=forms.TextInput(attrs={'class': 'money'}))

    def clean(self):
        data = super().clean()

        # Verificar rentabilidade
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        price = data.get('price')
        product_price = None
        product_multiple = None

        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
            except:
                self.add_error('product_id', 'Produto inválido.')

            product_price = product.price
            product_multiple = product.multiple

        order_helper = OrderHelper()

        # Verificar rentabilidade
        if price is not None and product_price is not None and \
                order_helper.get_profitability(price, product_price) < 0:
            self.add_error('price', 'Rentabilidade ruim.')

        # Verificar multiplos
        if quantity is not None and product_multiple is not None and \
                quantity % product_multiple != 0:
            self.add_error('quantity', 'Quantidade deve ser múltipla de '
                f'{product_multiple}.')

        return data
