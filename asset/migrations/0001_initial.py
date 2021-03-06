# Generated by Django 3.2.8 on 2021-10-12 13:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assettype',
            fields=[
                ('assettype_pk', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_pk', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=30)),
                ('staff_number', models.CharField(max_length=15)),
                ('staff_email', models.EmailField(max_length=254)),
                ('department', models.CharField(max_length=30)),
                ('section', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=50)),
                ('vkey', models.CharField(default='vkey', max_length=50)),
                ('accepted', models.CharField(default='Pending', max_length=10)),
                ('hod_approval', models.CharField(default='Pending', max_length=10)),
                ('date_assigned', models.DateField(auto_now_add=True)),
                ('asset_serial', models.CharField(max_length=30)),
                ('date_changed', models.DateField(blank=True, default=None, null=True)),
                ('reason_changed', models.CharField(blank=True, max_length=60)),
                ('changed_by', models.CharField(blank=True, max_length=30)),
                ('assigned_by', models.CharField(max_length=30)),
                ('ticket', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('asset_assigned', models.CharField(default='Yes', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Comp',
            fields=[
                ('asset_pk', models.AutoField(primary_key=True, serialize=False)),
                ('asset_serial', models.CharField(max_length=50, unique=True)),
                ('asset_model', models.CharField(max_length=50)),
                ('asset_tag', models.CharField(blank=True, default=None, max_length=50)),
                ('mac_address', models.CharField(max_length=50)),
                ('cpu_name', models.CharField(blank=True, default=None, max_length=30)),
                ('domain', models.CharField(blank=True, default=None, max_length=5)),
                ('reason_no_domain', models.CharField(blank=True, default=None, max_length=30)),
                ('ram', models.CharField(blank=True, default=None, max_length=10)),
                ('os', models.CharField(blank=True, default=None, max_length=15)),
                ('adss', models.CharField(blank=True, default=None, max_length=5)),
                ('laps', models.CharField(blank=True, default=None, max_length=5)),
                ('wol', models.CharField(blank=True, default=None, max_length=5)),
                ('kaspersky', models.CharField(blank=True, default=None, max_length=5)),
                ('reason_no_kaspersky', models.CharField(blank=True, default=None, max_length=30)),
                ('ip_address', models.CharField(blank=True, default=None, max_length=15)),
                ('extension', models.CharField(blank=True, default=None, max_length=10)),
                ('condition', models.CharField(default='Working', max_length=20)),
                ('ict_approval', models.CharField(default='Pending', max_length=30)),
                ('reject_reason', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('approved_by', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('deployed_date', models.DateField(auto_now_add=True)),
                ('obso_date', models.DateField(blank=True, default=None, null=True)),
                ('obso_reason', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('obso_officer', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('assettype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.assettype')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.client')),
                ('deployed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hod',
            fields=[
                ('hod_pk', models.AutoField(primary_key=True, serialize=False)),
                ('hod_name', models.CharField(max_length=30)),
                ('hod_number', models.CharField(max_length=15)),
                ('hod_email', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('monitor_pk', models.AutoField(primary_key=True, serialize=False)),
                ('monitor_serial', models.CharField(blank=True, default=None, max_length=30)),
                ('monitor_model', models.CharField(blank=True, default=None, max_length=30)),
                ('monitor_tag', models.CharField(blank=True, default=None, max_length=30)),
                ('monitor_cpu', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('cpu_assigned', models.CharField(default='Yes', max_length=5)),
                ('date_deployed', models.DateField(auto_now_add=True)),
                ('deployed_by', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('date_changed', models.DateField(blank=True, default=None, null=True)),
                ('reason_changed', models.CharField(blank=True, default=None, max_length=60, null=True)),
                ('changed_by', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('status', models.CharField(default='WORKING', max_length=15)),
                ('ticket_number', models.CharField(blank=True, default=None, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('region_pk', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_pk', models.AutoField(primary_key=True, serialize=False)),
                ('ticket_number', models.CharField(max_length=30)),
                ('ticket_officer', models.CharField(max_length=30)),
                ('ticket_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_pk', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.region')),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('repair_pk', models.AutoField(primary_key=True, serialize=False)),
                ('cdate', models.DateField(auto_now_add=True)),
                ('problem', models.CharField(max_length=60)),
                ('solution', models.CharField(blank=True, max_length=60)),
                ('ticket_number', models.CharField(max_length=30)),
                ('status', models.CharField(blank=True, default='Pending', max_length=20, null=True)),
                ('officer_returned', models.CharField(blank=True, max_length=30)),
                ('rdate', models.DateField(blank=True, default=datetime.datetime(1900, 1, 1, 0, 0), null=True)),
                ('comp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.comp')),
                ('officer_assigned', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile_2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.region')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ict', models.BooleanField(default=False)),
                ('is_ict_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comp',
            name='monitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.monitor'),
        ),
        migrations.AddField(
            model_name='comp',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.region'),
        ),
        migrations.AddField(
            model_name='comp',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.station'),
        ),
        migrations.AddField(
            model_name='comp',
            name='ticket',
            field=models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.ticket'),
        ),
        migrations.AddField(
            model_name='client',
            name='hod',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.hod'),
        ),
    ]
