from django import forms
from .models import Customer, Ticket

class NewCustomerForm(forms.ModelForm):
     class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']
        # widgets = {'name': }

class NewTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['customer_id', 'due_date', 'month_interval', 'assigned_to']
        # fields = ['customer_id', 'due_date', 'location', 'notes', 'assigned_to']
