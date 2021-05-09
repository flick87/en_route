from django.shortcuts import render, redirect
from tracker.forms import *
from tracker.models import *
from django.contrib.auth.decorators import login_required
from itertools import chain #For linking querysets, see equipment view

def home(request):
    return render(request, 'tracker/index.html')

@login_required(redirect_field_name=None, login_url='login')
def create_ticket(request):
    form = NewTicketForm(request.POST or None)
    all_tickets = Ticket.objects.all()

    print(all_tickets)

    if form.is_valid():
        form.save()

    context = {'form': form}

    return render(request, 'tracker/create_ticket.html', context)

# create_order/view_order might be the same page in the end
@login_required(redirect_field_name=None, login_url='login')
def view_order(request):
    return render(request, 'tracker/index.html')


@login_required(redirect_field_name=None, login_url='login')
def view_tickets(request):
    tickets = Ticket.objects.all()
    print(tickets)

    context = {'tickets': tickets}

    return render(request, 'tracker/view_tickets.html', context)


@login_required(redirect_field_name=None, login_url='login')
def view_customers(request):
    customers = Customer.objects.all()

    context = {'customers': customers}
    return render(request, 'tracker/view_customers.html', context)

# create_customer/view_customer might be the same page in the end
@login_required(redirect_field_name=None, login_url='login')
def create_customer(request):
    form = NewCustomerForm(request.POST or None)
    all_customers = Customer.objects.all()
    print(all_customers)

    if form.is_valid():
        form.save()

    context = {'form': form, 'customers': all_customers}

    return render(request, 'tracker/create_customer.html', context)

@login_required(redirect_field_name=None, login_url='login')
def view_customer(request):
    return render(request, 'tracker/index.html')



@login_required(redirect_field_name=None, login_url='login')
def equipment(request):
    user = request.user

    if request.method == "POST":
        equipment = request.POST.getlist('equipment_name')
        if 'checkOutForm' in request.POST:
            take_ownership_of_items(equipment, user)
        if 'checkInForm' in request.POST:
            release_ownership_of_items(equipment, user)


    # NEED TO FIGURE OUT HOW YOU WANT TO LIST HARDWARE UNDER KITS
    kits = Kit.objects.all().filter(is_owned=True, owner=user)
    all_hardware = Hardware.objects.all()
    kit_hardware = all_hardware.filter(part_of_kit=True, is_owned=True, owner=user) #ALL KIT HW, not just a single kit
    loned_hardware = all_hardware.filter(part_of_kit=False, is_owned=True, owner=user)
    available_hardware = all_hardware.filter(is_owned=False)

    available_kits = Kit.objects.all().filter(is_owned=False)

    available_equipment = list(chain(available_kits, available_hardware))

    # figure out how to list hardware objects that belong to a kit below the kit in some manner in the html,
    # but not selectable.

    user_equipment = list(chain(kits, loned_hardware, kit_hardware))
    post_data = {}

    context = {'equipment': user_equipment, 'available_hardware': available_equipment}

    return render(request, 'tracker/equipment.html', context)









# NEED TO MAKE HARDWARE IN KITS NOT SELECTABLE SO THAT THE QUERIES FOR HARDWARES & KITS CAN BE FILTERED PROPERLY BY OWNED AND OWNER
def release_ownership_of_items(equipment_list, user):
    hardwares = Hardware.objects.all()
    kits = Kit.objects.all()
    for item in equipment_list:
        equipment_type, id_number = item.split(' ')
        if equipment_type == "Kit:":
            release_ownership(user, kits.filter(pk=id_number).first())
            kit_hardware = hardwares.filter(part_of_kit=True, kit_id=id_number)
            for hw in kit_hardware:
                release_ownership(user, hw)
        else:
            release_ownership(user, hardwares.filter(pk=id_number).first())


def take_ownership_of_items(equipment_list, user):
    print("PRINTING EQUIPMENT_LIST")
    print(equipment_list)
    hardwares = Hardware.objects.all().filter()
    kits = Kit.objects.all().filter()
    for item in equipment_list:
        equipment_type, id_number = item.split(' ')
        if equipment_type == "Kit:":
            take_ownership(user, kits.filter(pk=id_number).first())
            kit_hardware = hardwares.filter(part_of_kit=True, kit_id=id_number)
            for hw in kit_hardware:
                take_ownership(user, hw)
        else:
            take_ownership(user, hardwares.filter(pk=id_number).first())


# Equipment must have is_owned and user
def take_ownership(user, equipment):
    equipment.is_owned = True
    equipment.owner = user
    equipment.save()


def release_ownership(user, equipment):
    equipment.is_owned = False
    equipment.save()
