from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

from ..forms import ItemFormset


# Default invoice list, show recent invoices by the date it was created.
from invoice.models.customer import Customer
from invoice.models.inv import Invoice


@login_required(login_url='users:login')
def index(request):
    invoice = Invoice.objects.all().order_by('-date_created')
    page = request.GET.get('page', 1)

    paginator = Paginator(invoice, 25)
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    context = {
        'title': 'Recent Invoices',
        'invoice_list': invoices,
    }
    return render(request, 'invoice/index.html', context)


# Show big list of all invoices
@login_required(login_url='users:login')
def all_invoices(request):
    invoice = Invoice.objects.filter().order_by('-date_created') #All invoices considered as just the valid ones
    page = request.GET.get('page', 1)

    paginator = Paginator(invoice, 25)
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    context = {
        'title': 'All Invoices',
        'invoice_list': invoices,
    }
    return render(request, 'invoice/all_invoice.html', context=context)


# Show draft invoices
@login_required(login_url='users:login')
def draft_invoices(request):
    invoice = Invoice.objects.filter(status='Draft').order_by('-date_created')
    page = request.GET.get('page', 1)

    paginator = Paginator(invoice, 25)
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    context = {
        'title': 'Draft Invoices',
        'invoice_list': invoices,
    }
    return render(request, 'invoice/index.html', context)


# Show invalid invoices
@login_required(login_url='users:login')
def invalid_invoices(request):
    invoice = Invoice.objects.filter(valid=False).order_by('-date_created')
    page = request.GET.get('page', 1)

    paginator = Paginator(invoice, 25)
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    context = {
        'title': 'Invalid Invoices',
        'invoice_list': invoices,
    }
    return render(request, 'invoice/invalid_invoices.html', context)


# Show paid invoices
@login_required(login_url='users:login')
def paid_invoices(request):
    invoice = Invoice.objects.filter(status='Paid').order_by('-date_created')
    page = request.GET.get('page', 1)

    paginator = Paginator(invoice, 25)
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    context = {
        'title': 'Paid Invoices',
        'invoice_list': invoices,
    }
    return render(request, 'invoice/paid_invoices.html', context)


# Show unpaid invoices
@login_required(login_url='users:login')
def unpaid_invoices(request):
    invoice = Invoice.objects.filter(status='Unpaid').order_by('-date_created')
    page = request.GET.get('page', 1)

    paginator = Paginator(invoice, 25)
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    context = {
        'title': 'Unpaid Invoices',
        'invoice_list': invoices,
    }
    return render(request, 'invoice/unpaid_invoices.html', context)


# Display a specific invoice
@login_required(login_url='users:login')
def invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)

    itemformset = ItemFormset()
    context = {
        'title': 'Invoice ' + invoice_id,
        'invoice': invoice,
        'formset': itemformset, 
    }
    return render(request, 'invoice/invoice.html', context)


# Search for invoice
@login_required(login_url='users:login')
def search_invoice(request):
    invoice_number = request.POST['invoice_number']  
    return HttpResponseRedirect(reverse('invoice:view_invoice', args=(invoice_number,)))


# Create new invoice
@login_required(login_url='users:login')
def new_invoice(request):
        # If no customer_id is defined, create a new invoice
    if request.method == 'POST':
        customer_id = request.POST.get("customer_id", "None")
        invoice_number = request.POST.get('invoice_number')
        due_date = request.POST.get("expiration_date", datetime.date.today() + datetime.timedelta(days=7))
        status = request.POST.get("status", 'Unpaid')

        if customer_id == 'None':
            customers = Customer.objects.order_by('name')
            context = {
                'title': 'New Invoice',
                'customer_list': customers,
                'error_message': 'Please select a customer.',
            }
            return render(request, 'invoice/new_invoice.html', context)
        else:
            customer = get_object_or_404(Customer, pk=customer_id)
            i = Invoice(customer=customer, invoice_number=invoice_number,
                        due_date=due_date, status=status)
            i.save()
            return HttpResponseRedirect(reverse('invoice:invoice', args=(i.invoice_number,)))

    else:
        # Customer list needed to populate select field
        customers = Customer.objects.order_by('name')
        context = {
            'title': 'New Invoice',
            'customer_list': customers,
        }
        return render(request, 'invoice/new_invoice.html', context)


# View invoice
@login_required(login_url='users:login')
def view_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)
    context = {
        'title': "Invoice " + invoice_id,
        'invoice': invoice,
    }
    return render(request, 'invoice/view_invoice.html', context)


# Print invoice
@login_required(login_url='users:login')
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)
    context = {
        'title': "Invoice " + invoice_id,
        'invoice': invoice,
    }
    return render(request, 'invoice/print_invoice.html', context)


# clear/pay off invoice
def clear_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)
    invoice.status = 'Paid'
    invoice.save()
    return HttpResponseRedirect(reverse('invoice:index'))



# Invalidate an invoice
@login_required(login_url='users:login')
def invalidate_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)
    invoice.valid = False
    invoice.save()
    return HttpResponseRedirect(reverse('invoice:index'))
