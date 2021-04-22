from django.shortcuts import render, redirect
from .forms import *

def home(request):
    return render(request, 'tracker/index.html')

def create_order(request):
    return render(request, 'tracker/create_order.html')

# create_order/view_order might be the same page in the end
def view_order(request):
    return render(request, 'tracker/index.html')

def view_orders(request):
    return render(request, 'tracker/index.html')

def view_customers(request):
    return render(request, 'tracker/index.html')

# create_customer/view_customer might be the same page in the end
def create_customer(request):
    form = NewCustomerForm(request.POST or None)

    if form.is_valid():
        print("This is where you will save/update database")
        return redirect('tracker-home')

    context = {'form': form}

    return render(request, 'tracker/create_customer.html', context)

def view_customer(request):
    return render(request, 'tracker/index.html')
