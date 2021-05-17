from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal

from order.models import *
from order.forms import *
from lib.order import *


""" Listar pedidos """
def index(request):
    orders = Order.objects.all()

    context = {
        'orders': orders
    }
    return render(request, 'order/index.html', context)

""" Criar pedido """
def create(request):
    order_helper = OrderHelper()
    form = OrderForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            try:
                order = Order.objects.create(**data)
            except Exception as e:
                messages.error(request, f'Erro ao criar pedido. {e}')
            else:
                return redirect('order-detail', id_=order.pk)

    context = {
        'form': form
    }
    return render(request, 'order/create.html', context)

""" Detalhes do pedido """
def detail(request, id_):
    order_helper = OrderHelper()

    # Selecionar o pedido
    try:
        order = Order.objects.get(pk=id_)
    except:
        messages.error(request, 'Pedido não encontrado.')
        return redirect('order-index')
    
    # Retornar lista de itens
    items = order.items.all()

    # Alterar pedido
    if 'order-update' in request.POST:
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            data = order_form.cleaned_data

            try:
                order.client = data['client']
                order.save()
            except:
                messages.error(request, 'Erro ao alterar pedido.')
            else:
                messages.success(request, 'Cliente alterado com sucesso.')
                return redirect('order-detail', id_=id_)
    else:
        order_form = OrderForm(None, initial={'client': order.client})

    # Adicionar item
    if 'item-create' in request.POST:
        request_post = request.POST.dict()
        request_post['price'] = request_post.get('price', '').replace('.', '')

        item_form = ItemForm(request_post)

        if item_form.is_valid():
            data = item_form.cleaned_data

            try:
                order_helper.item_create(id_, **data)
            except Exception as e:
                messages.error(request, e)
            else:
                return redirect('order-detail', id_=id_)
    else:
        item_form = ItemForm(None)

    # Remover item
    if 'item-delete' in request.POST:
        item_id = request.POST.get('item')

        try:
            order_helper.item_delete(item_id)
        except Exception as e:
            messages.error(request, e)
        else:
            return redirect('order-detail', id_=id_)

    context = {
        'order_form': order_form,
        'item_form': item_form,
        'order': order,
        'items': items
    }
    return render(request, 'order/detail.html', context)
