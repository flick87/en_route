from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Kit(models.Model):
    kit_id          = models.AutoField(primary_key=True, unique=True)
    name            = models.CharField(max_length=55)
    location        = models.CharField(max_length=254, default="default")
    is_owned        = models.BooleanField(blank=False, default=False)
    owner           = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.name

class Hardware(models.Model):
    hw_id           = models.AutoField(primary_key=True, unique=True)
    name            = models.CharField(max_length=55)
    serial_number   = models.CharField(max_length=128, null=True)
    part_number     = models.CharField(max_length=128, null=True)
    kit_id          = models.ForeignKey('Kit', on_delete=models.RESTRICT, null=True)
    location        = models.CharField(max_length=254, default="default")

    def __str__(self):
        return self.name

class Software(models.Model):
    sw_id           = models.AutoField(primary_key=True, unique=True)
    hw_id           = models.ForeignKey('Hardware', on_delete=models.RESTRICT, null=True)
    name            = models.CharField(max_length=55)
    version         = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer_id     = models.AutoField(primary_key=True, unique=True)
    name            = models.CharField(max_length=55)
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")
    phone           = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    email           = models.EmailField(max_length=254)
    address         = models.CharField(max_length=255, default="default")
    customer_origin = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    ticket_id       = models.AutoField(primary_key=True, unique=True)
    customer_id     = models.ForeignKey('Customer', on_delete=models.RESTRICT)
    date_created    = models.DateTimeField(default=timezone.now)
    due_date        = models.DateTimeField()
    date_completed  = models.DateTimeField(null=True)
    location        = models.CharField(max_length=254)
    interval        = models.IntegerField(default=0)
    is_completed    = models.BooleanField(blank=False, default=False)
    notes           = models.CharField(max_length=254, blank=True)
    kit_id          = models.ForeignKey('Kit', on_delete=models.RESTRICT, null=True)
    assigned_to     = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.date_created

class Log(models.Model):
    log_id          = models.AutoField(primary_key=True, unique=True)
    hw_id           = models.ForeignKey('Hardware', on_delete=models.RESTRICT, null=True)
    kit_id          = models.ForeignKey('Kit', on_delete=models.RESTRICT, null=True)
    event_type      = models.CharField(max_length=25, blank=True)
    event           = models.CharField(max_length=254)
    date            = models.DateTimeField(default=timezone.now)
    author          = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.event
