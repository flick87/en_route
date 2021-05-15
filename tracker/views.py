from django.shortcuts import render, redirect
from tracker.forms import *
from tracker.models import *
from django.contrib.auth.decorators import login_required
from itertools import chain #For linking querysets, see equipment view

def home(request):
    return render(request, 'tracker/index.html')

@login_required(redirect_field_name=None, login_url='login')
def create_ticket(request):
    form              = NewTicketForm(request.POST or None)
    all_tickets       = Ticket.objects.all()
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
    search_form       = TicketSearchForm(initial={'search_date':'None', 'employee_select': 'None', 'customer_select': 'None'})
    user              = request.user
    all_tickets       = Ticket.objects.all()
    user_tickets      = all_tickets.filter(is_completed=False, assigned_to=user)
    available_tickets = all_tickets.filter(is_completed=False, assigned_to=None)
    # Build filters here
    if request.method == 'POST':
        if 'search_form' in request.POST:
            search_form = TicketSearchForm(request.POST)
        tickets     = request.POST.getlist('ticket_ids')
        if search_form.is_valid():
            cleaned_form      = get_cleaned_filter_search(search_form)
            available_tickets = filter_tickets(cleaned_form)
        elif 'assign_ticket' in request.POST:
            assign_tickets(tickets, user)
        elif 'unassign_ticket' in request.POST:
            unassign_tickets(tickets, user)

    # Grey tickets out if they show in filter and are owned by another user
    context = {'available_tickets': available_tickets, 'user_tickets': user_tickets, 'search_form': search_form}
    return render(request, 'tracker/view_tickets.html', context)










@login_required(redirect_field_name=None, login_url='login')
def view_customers(request):
    customers = Customer.objects.all()
    contacts = []
    customer = Customer()
    customer_form = NewCustomerForm()
    if request.method == 'POST':
        if 'customer_select_button' in request.POST:
            customer = customers.filter(pk=request.POST['customer_select_button']).first()
            customer_form = NewCustomerForm(instance=customer)
            request.session['selected_customer'] = customer.id
        elif 'customer_save_button' in request.POST:
            customer_form = NewCustomerForm(request.POST, instance=Customer.objects.all().filter(pk=request.session['selected_customer']).first())
            if customer_form.is_valid():
                customer_form.save()
        contacts = Contact.objects.all().filter(customer_id=request.session['selected_customer'])
    context   = {'customers': customers, 'customer': customer, 'customer_form': customer_form, 'contacts': contacts}
    return render(request, 'tracker/view_customers.html', context)


















# create_customer/view_customer might be the same page in the end
@login_required(redirect_field_name=None, login_url='login')
def create_customer(request):
    form = NewCustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
    all_customers = Customer.objects.all()
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







# ***************************************** Helper Functions Below *****************************************************************



def filter_tickets(cleaned_form):
    tickets = Ticket.objects.all().filter(assigned_to=None)
    null_str = 'None'
    if cleaned_form['assignee'] != null_str:
        tickets = tickets.filter(assigned_to=cleaned_form['assignee'])
    if cleaned_form['customer'] != null_str:
        tickets = tickets.filter(customer_id=cleaned_form['customer'])
    if cleaned_form['date_search_type'] != null_str:
        if cleaned_form['date_search_type'] == 'Date Created':
            if cleaned_form['start_date'] != None and cleaned_form['end_date'] != None:
                tickets = tickets.filter(date_created__range=(cleaned_form['start_date'], cleaned_form['end_date'] + timedelta(days=1)) )
            elif cleaned_form['start_date'] != None and cleaned_form['end_date'] == None:
                tickets = tickets.filter(date_created__gte=cleaned_form['start_date'])
            elif cleaned_form['start_date'] == None and cleaned_form['end_date'] != None:
                tickets = tickets.filter(date_created__lse=cleaned_form['end_date'])
            tickets.order_by('-date_created')
        elif cleaned_form['date_search_type'] == 'Due Date':
            if cleaned_form['start_date'] != None and cleaned_form['end_date'] != None:
                tickets = tickets.filter(due_date__range=(cleaned_form['start_date'], cleaned_form['end_date'] + timedelta(days=1)) )
            elif cleaned_form['start_date'] != None and cleaned_form['end_date'] == None:
                tickets = tickets.filter(due_date__gte=cleaned_form['start_date'])
            elif cleaned_form['start_date'] == None and cleaned_form['end_date'] != None:
                tickets = tickets.filter(due_date__lte=cleaned_form['end_date'])
            tickets.order_by('-due_date')
        elif cleaned_form['date_search_type'] == 'Date Completed':
            tickets = tickets.exclude(date_completed__isnull=True)
            if cleaned_form['start_date'] != None and cleaned_form['end_date'] != None:
                tickets = tickets.filter(date_completed__range=(cleaned_form['start_date'], cleaned_form['end_date'] + timedelta(days=1)) )
            elif cleaned_form['start_date'] != None and cleaned_form['end_date'] == None:
                tickets = tickets.filter(date_completed__gte=cleaned_form['start_date'])
            elif cleaned_form['start_date'] == None and cleaned_form['end_date'] != None:
                tickets = tickets.filter(date_completed__lte=cleaned_form['end_date'])
            tickets.order_by('-date_completed')
        # elif cleaned_form['date_search_type'] == 'Date Assigned':
        #     tickets = tickets.exclude(date_assigned__isnull=True)
        #     if cleaned_form['start_date'] != None and cleaned_form['end_date'] != None:
        #         tickets = tickets.filter(date_assigned__range=(cleaned_form['start_date'], cleaned_form['end_date'] + timedelta(days=1)) )
        #     elif cleaned_form['start_date'] != None and cleaned_form['end_date'] == None:
        #         tickets = tickets.filter(date_assigned__gte=cleaned_form['start_date'])
        #     elif cleaned_form['start_date'] == None and cleaned_form['end_date'] != None:
        #         tickets = tickets.filter(date_assigned__lte=cleaned_form['end_date'])
        #     tickets.order_by('-date_assigned')
    return tickets



def get_cleaned_filter_search(search_form):
    to_return = {
        'date_search_type': search_form.cleaned_data.get('search_date'),
        'assignee': search_form.cleaned_data.get('employee_select'), # <------- This should be removed. This is for functionality with the admin account
        'customer': search_form.cleaned_data.get('customer_select'),
        'start_date': search_form.cleaned_data.get('start_date'),
        'end_date': search_form.cleaned_data.get('end_date'),
        # 'date_assigned': search_form.cleaned_data.get('date_assigned')
    }
    return to_return


# NEED TO MAKE HARDWARE IN KITS NOT SELECTABLE SO THAT THE QUERIES FOR HARDWARES & KITS CAN BE FILTERED PROPERLY BY OWNED AND OWNER
# Refactor
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
        elif equipment_type == "Hardware:":
            release_ownership(user, hardwares.filter(pk=id_number).first())

# Refactor
def take_ownership_of_items(equipment_list, user):
    hardwares = Hardware.objects.all()
    kits = Kit.objects.all().filter()
    for item in equipment_list:
        equipment_type, id_number = item.split(' ')
        if equipment_type == "Kit:":
            take_ownership(user, kits.filter(pk=id_number).first())
            kit_hardware = hardwares.filter(part_of_kit=True, kit_id=id_number)
            for hw in kit_hardware:
                take_ownership(user, hw)
        elif equipment_type == "Hardware:":
            take_ownership(user, hardwares.filter(pk=id_number).first())

# Equipment must have is_owned and user
def take_ownership(user, equipment):
    equipment.is_owned = True
    equipment.owner = user
    equipment.save()


def release_ownership(user, equipment):
    equipment.is_owned = False
    equipment.save()

def assign_tickets(ticket_ids, user):
    query = Ticket.objects.all()
    for ticket_id in ticket_ids:
        ticket = query.filter(pk=ticket_id).first()
        assign_ticket(ticket, user)
        create_ticket_log(ticket, user, 'assign')

def unassign_tickets(ticket_ids, user):
    query = Ticket.objects.all()
    for ticket_id in ticket_ids:
        ticket = query.filter(pk=ticket_id).first()
        unassign_ticket(ticket)
        create_ticket_log(ticket, user, 'unassign')

def assign_ticket(ticket, user):
    ticket.assigned_to = user
    ticket.date_assigned = datetime.date.today()
    ticket.save()

def unassign_ticket(ticket):
    ticket.assigned_to = None
    ticket.date_assigned = None
    ticket.save()





# ************************************ Logs ******************************************
def create_ticket_log(ticket, user, flag):
    print("Create ticket log. " + flag)
