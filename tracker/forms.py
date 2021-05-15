from django import forms
from .models import Customer, Ticket
from django.contrib.auth.models import User

class DateFieldInput(forms.DateInput):
    input_type      = 'date'

class NewCustomerForm(forms.ModelForm):
     class Meta:
        model       = Customer
        fields      = ['name', 'phone', 'email']

class NewTicketForm(forms.ModelForm):
    class Meta:
        widgets     = {'due_date': DateFieldInput() }
        model       = Ticket
        fields      = ['customer_id', 'due_date', 'month_interval', 'assigned_to']
        # fields = ['customer_id', 'due_date', 'location', 'notes', 'assigned_to']


class TicketSearchForm(forms.Form):
    tickets          = Ticket.objects.all()
    customers        = Customer.objects.all()
    users            = User.objects.all()

    customer_choices = [ (customer.id, customer.name) for customer in customers ]
    customer_choices.insert(0, ('None','None'))
    user_choices     = [ (user.id, user) for user in users ]
    user_choices.insert(0, ('None','None'))
    # date_choices     = [('None','None'), ('Date Created', 'Date Created'), ('Date Completed','Date Completed'), ('Due Date', 'Due Date'), ('Date Assigned', 'Date Assigned')]
    date_choices     = [('None','None'), ('Date Created', 'Date Created'), ('Date Completed','Date Completed'), ('Due Date', 'Due Date')]

    employee_select  = forms.ChoiceField(required=False, choices=user_choices)
    customer_select  = forms.ChoiceField(required=False, choices=customer_choices)
    search_date      = forms.ChoiceField(widget=forms.RadioSelect, choices=date_choices)
    start_date       = forms.DateField(widget=DateFieldInput, required=False)
    end_date         = forms.DateField(widget=DateFieldInput, required=False)
    field_order      = ['assignee', 'employee_select', 'customer', 'customer_select', 'search_date', 'date']
