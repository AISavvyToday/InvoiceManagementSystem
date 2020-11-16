from django.conf.urls import url
from .views import invoices, items, customers

app_name = 'invoicemanager'

urlpatterns = [

    url(r'^$', invoices.index, name='index'),

    # INVOICES
    url(r'^invoice/new/$', invoices.new_invoice, name='new_invoice'),
    url(r'^invoice/all/$', invoices.all_invoices, name='all_invoices'),
    url(r'^invoice/draft/$', invoices.draft_invoices, name='draft_invoices'),
    url(r'^invoices/invalid/$', invoices.invalid_invoices, name='invalid_invoices'),
    url(r'^invoice/paid/$', invoices.paid_invoices, name='paid_invoices'),
    url(r'^invoice/unpaid/$', invoices.unpaid_invoices, name='unpaid_invoices'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/$', invoices.invoice, name='invoice'),
    url(r'^invoice/search/$', invoices.search_invoice, name='search_invoice'),
    url(r'^view-invoice/(?P<invoice_id>[0-9]+)/$', invoices.view_invoice, name='view_invoice'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/print/$', invoices.print_invoice, name='print_invoice'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/print/download_invoice$', invoices.download_invoice, name='download_invoice'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/clear/$', invoices.clear_invoice, name='clear_invoice'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/invalidate/$', invoices.invalidate_invoice, name='invalidate_invoice'),

    # ITEMS
    url(r'^invoice/(?P<invoice_id>[0-9]+)/item/add/$', items.add_item, name='add_item'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/item/(?P<invoiceitem_id>[0-9]+)/delete/$', items.delete_item, name='delete_item'),

    # CUSTOMERS
    url(r'^customers/$', customers.customer_list, name='customer_list'),
    url(r'^customer/(?P<customer_id>[0-9]+)/$', customers.customer, name='customer'),
    url(r'^customer/(?P<customer_id>[0-9]+)/update/$', customers.update_customer, name='update_customer'),
    url(r'^customer/(?P<customer_id>[0-9]+)/delete/$', customers.delete_customer, name='delete_customer'),
    url(r'^customer/new/$', customers.new_customer, name='new_customer'),
]
