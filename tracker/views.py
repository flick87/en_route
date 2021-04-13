from django.shortcuts import render

def home(request):
    return render(request, 'tracker/index.html')

def create_order(request):
    return render(request, 'tracker/index.html')

# create_order/view_order might be the same page in the end
def view_order(request):
    return render(request, 'tracker/index.html')

def view_orders(request):
    return render(request, 'tracker/index.html')

def view_customers(request):
    return render(request, 'tracker/index.html')

# create_customer/view_customer might be the same page in the end
def create_customer(request):
    return render(request, 'tracker/index.html')

def view_customer(request):
    return render(request, 'tracker/index.html')
