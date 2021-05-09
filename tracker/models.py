from django.db import models
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

phone_regex         = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")

class Address(models.Model):
    street          = models.CharField(max_length=255)
    unit            = models.CharField(max_length=255, null=True, blank=True, default="")
    city            = models.CharField(max_length=255)
    state           = models.CharField(max_length=255)
    zipcode         = models.CharField(max_length=255)

    def __str__(self):
        return self.street + ",\n" + self.city + " " + self.state + ", " + self.zipcode

class Vendor(models.Model):
    address         = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)
    phone           = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    name            = models.CharField(max_length=55)

    def __str__(self):
        return self.name

class Kit(models.Model):
    name            = models.CharField(max_length=55)
    location        = models.CharField(max_length=254, default="default")
    address         = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)
    is_owned        = models.BooleanField(blank=False, default=False)
    owner           = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return "Kit: " + str(self.id)

class Hardware(models.Model):
    kit_id          = models.ForeignKey(Kit, on_delete=models.RESTRICT, null=True, blank=True)
    owner           = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    part_of_kit     = models.BooleanField(blank=True, default=False)
    name            = models.CharField(max_length=55, blank=True)
    serial_number   = models.CharField(max_length=128, null=True, blank=True, default="NNN")
    model           = models.CharField(max_length=128, null=True, blank=True, default="NNN")
    part_number     = models.CharField(max_length=128, null=True, blank=True)
    decommissioned  = models.BooleanField(blank=True, default=False)
    is_owned        = models.BooleanField(blank=True, default=False)
    location        = models.CharField(max_length=254, default="default")
    address         = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return "Hardware: " + str(self.id)


class Software(models.Model):
    hardware_id     = models.ForeignKey(Hardware, on_delete=models.RESTRICT, null=True, blank=True)
    name            = models.CharField(max_length=55, blank=True)
    version         = models.CharField(max_length=55)
    serial_number   = models.CharField(max_length=128, null=True, blank=True, default="NNN")
    model           = models.CharField(max_length=128, null=True, blank=True, default="NNN")
    date_installed  = models.DateField(default=datetime.date.today())
    is_installed    = models.BooleanField(blank=True, default=False)
    decommissioned  = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name

class Consumable(models.Model):
    id              = models.AutoField(primary_key=True, unique=True)
    name            = models.CharField(max_length=55)
    quantity        = models.IntegerField(default=1)
    date_refilled   = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.name + ", Quantity: " + str(self.quantity)

class Purchase(models.Model):
    vendor_id       = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True, blank=True)
    consumable_id   = models.ForeignKey(Consumable, on_delete=models.RESTRICT, null=True, blank=True)
    software_id     = models.ForeignKey(Software, on_delete=models.RESTRICT, null=True, blank=True)
    hardware_id     = models.ForeignKey(Hardware, on_delete=models.RESTRICT, null=True, blank=True)

    is_consumable   = models.BooleanField(blank=True, default=False, null=True)
    is_hardware     = models.BooleanField(blank=True, default=False, null=True)
    is_software     = models.BooleanField(blank=True, default=False, null=True)

    quantity        = models.IntegerField(default=1)
    cost            = models.IntegerField(default=0)
    date_purchased  = models.DateField(default=datetime.date.today())
    # PDF??????????????????????????????????????????????????????????????????????????????????

    # FIX ME
    def __str__(self):
        edit_str = ""
        if self.is_consumable:
            return "Consumable " + str(self.consumable_id) + " was purchased on " + str(self.date_purchased) + " for  $" + str(self.cost)
        elif self.is_hardware:
            return "Hardware " + str(self.hardware_id) + " was purchased on " + str(self.date_purchased) + " for  $" + str(self.cost)
        return "Software " + str(self.software_id) + " was purchased on " + str(self.date_purchased) + " for  $" + str(self.cost)


class Warranty(models.Model):
    hardware_id     = models.ForeignKey(Hardware, on_delete=models.RESTRICT, null=True, blank=True)
    software_id     = models.ForeignKey(Software, on_delete=models.RESTRICT, null=True, blank=True)
    is_hardware     = models.BooleanField(blank=True, default=False)
    is_software     = models.BooleanField(blank=True, default=False)
    date_issued     = models.DateField(default=datetime.date.today())
    expiration_date = models.DateField(default=datetime.date.today())
    date_purchased  = models.DateField(default=datetime.date.today())
    cost            = models.BigIntegerField(default=0)
    # PDF??????????????????????????????????????????????????????????????????????????????????

    # FIX ME
    def __str__(self):
        edit_str = ""
        if self.is_hardware:
            return "Warranty for Hardware " + str(self.hardware_id) + " expires on " + str(self.expiration_date)
        return "Warranty for Software " + str(self.software_id) + " expires on " + str(self.expiration_date)


class Customer(models.Model):
    id     = models.AutoField(primary_key=True, unique=True)
    address         = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True)
    name            = models.CharField(max_length=55)
    phone           = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email           = models.EmailField(max_length=50, blank=True)
    customer_origin = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.name

class Contact(models.Model):
    address         = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)
    customer_id     = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True, blank=True)
    vendor_id       = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True, blank=True)
    is_customer     = models.BooleanField(blank=True, default=False)
    is_vendor       = models.BooleanField(blank=True, default=False)
    phone           = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    first           = models.CharField(max_length=20)
    last            = models.CharField(max_length=20)
    origin          = models.DateField(default=datetime.date.today())
    email           = models.EmailField(max_length=50)
    # NOTES ******************************************* ?????????????????????????????????

    def __str__(self):
        return self.first + " " + self.last


class Ticket(models.Model):
    ticket_id       = models.AutoField(primary_key=True, unique=True)
    customer_id     = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    assigned_to     = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    address         = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)
    date_created    = models.DateField(default=datetime.date.today())
    due_date        = models.DateField(default=datetime.date.today() + relativedelta(months=12))
    date_completed  = models.DateField(null=True, blank=True)
    month_interval  = models.IntegerField(default=0)
    is_completed    = models.BooleanField(blank=False, default=False)
    # NOTES ******************************************* ?????????????????????????????????

    def __str__(self):
        return self.customer_id.name

class Note(models.Model):
    address_id      = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)
    customer_id     = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True, blank=True)
    vendor_id       = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True, blank=True)
    consumable_id   = models.ForeignKey(Consumable, on_delete=models.RESTRICT, null=True, blank=True)
    software_id     = models.ForeignKey(Software, on_delete=models.RESTRICT, null=True)
    hardware_id     = models.ForeignKey(Hardware, on_delete=models.RESTRICT, null=True)
    kit_id          = models.ForeignKey(Kit, on_delete=models.RESTRICT, null=True)
    ticket_id       = models.ForeignKey(Ticket, on_delete=models.RESTRICT, null=True)
    warranty_id     = models.ForeignKey(Warranty, on_delete=models.RESTRICT, null=True)
    purchase_id     = models.ForeignKey(Purchase, on_delete=models.RESTRICT, null=True)

    is_consumable   = models.BooleanField(blank=True, default=False, null=True)
    is_hardware     = models.BooleanField(blank=True, default=False, null=True)
    is_software     = models.BooleanField(blank=True, default=False, null=True)
    is_customer     = models.BooleanField(blank=True, default=False, null=True)
    is_vendor       = models.BooleanField(blank=True, default=False, null=True)
    is_address      = models.BooleanField(blank=True, default=False, null=True)
    is_contact      = models.BooleanField(blank=True, default=False, null=True)
    is_kit          = models.BooleanField(blank=True, default=False, null=True)
    is_warranty     = models.BooleanField(blank=True, default=False, null=True)
    is_purchase     = models.BooleanField(blank=True, default=False, null=True)

    details         = models.CharField(max_length=55)
    date            = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.details

class Log(models.Model):
    address_id      = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)
    customer_id     = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True, blank=True)
    vendor_id       = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True, blank=True)
    consumable_id   = models.ForeignKey(Consumable, on_delete=models.RESTRICT, null=True, blank=True)
    software_id     = models.ForeignKey(Software, on_delete=models.RESTRICT, null=True)
    hardware_id     = models.ForeignKey(Hardware, on_delete=models.RESTRICT, null=True)
    kit_id          = models.ForeignKey(Kit, on_delete=models.RESTRICT, null=True)
    ticket_id       = models.ForeignKey(Ticket, on_delete=models.RESTRICT, null=True)
    warranty_id     = models.ForeignKey(Warranty, on_delete=models.RESTRICT, null=True)
    purchase_id     = models.ForeignKey(Purchase, on_delete=models.RESTRICT, null=True)

    date            = models.DateTimeField(default=timezone.now)
    author          = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.event
