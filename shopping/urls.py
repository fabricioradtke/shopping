from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from order import views as order_views


urlpatterns = [
    path('', order_views.index, name='order-index'),
    path('pedido/adicionar/', order_views.create, name='order-create'),
    path('pedido/<int:id_>/itens/', order_views.detail, name='order-detail'),
]

urlpatterns += staticfiles_urlpatterns()
