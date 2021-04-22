# Generated by Django 3.1.6 on 2021-04-21 23:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20210414_2043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hardware',
            old_name='hw_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='reoccuring',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(default='default', max_length=255),
        ),
        migrations.AddField(
            model_name='hardware',
            name='location',
            field=models.CharField(default='default', max_length=254),
        ),
        migrations.AddField(
            model_name='kit',
            name='location',
            field=models.CharField(default='default', max_length=254),
        ),
        migrations.AddField(
            model_name='ticket',
            name='date_completed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='kit_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='tracker.kit'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='location',
            field=models.CharField(max_length=254),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('event_type', models.CharField(blank=True, max_length=25)),
                ('event', models.CharField(max_length=254)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('hw_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='tracker.hardware')),
                ('kit_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='tracker.kit')),
            ],
        ),
    ]
