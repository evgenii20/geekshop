import ordersapp.views as ordersapp

from django.urls import path

app_name = 'ordersapp'

urlpatterns = [
    # re_path(r'^$', ordersapp.OrderList.as_view(), name='orders_list'),
    path('', ordersapp.OrderListView.as_view(), name='orders_list'),
    # re_path(r'^create/$', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='orders_create'),
    # re_path(r'^read/(?P<pk>\d+)/$', ordersapp.OrderRead.as_view(), name='order_read'),
    path('read/<int:pk>/', ordersapp.OrderDetailView.as_view(), name='orders_detail'),
    # re_path(r'^update/(?P<pk>\d+)/$', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    path('update/<int:pk>/', ordersapp.OrderUpdateView.as_view(), name='orders_update'),
    # re_path(r'^delete/(?P<pk>\d+)/$', ordersapp.OrderDelete.as_view(), name='order_delete'),
    path('delete/<int:pk>/', ordersapp.OrderDeleteView.as_view(), name='orders_delete'),

    # re_path(r'^forming/complete/(?P<pk>\d+)/$', ordersapp.order_forming_complete, name='order_forming_complete'),
    path('forming/complete/<int:pk>/', ordersapp.order_forming_complete, name='orders_forming_complete'),
]
