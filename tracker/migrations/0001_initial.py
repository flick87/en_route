# Generated by Django 3.1.6 on 2021-04-13 22:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=55)),
                ('phone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('customer_origin', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('hw_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('hw_name', models.CharField(max_length=55)),
                ('serial_number', models.CharField(max_length=128, null=True)),
                ('part_number', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('kit_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=55)),
                ('is_owned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('reoccuring', models.BooleanField(default=False)),
                ('interval', models.IntegerField(default=0)),
                ('is_completed', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, max_length=254)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tracker.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('sw_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=55)),
                ('version', models.CharField(max_length=55)),
                ('hw_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='tracker.hardware')),
            ],
        ),
        migrations.AddField(
            model_name='hardware',
            name='kid_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='tracker.kit'),
        ),
    ]