from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Profile Model


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_ict = models.BooleanField(default=False)
    is_ict_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"Is ICT Staff - {self.is_ict}, Is ICT Admin - {self.is_ict_admin}, {self.user.username}, {self.user.profile_2.name} "

# Region model


class Region(models.Model):
    region_pk = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, unique=True)

    class Meta:
        ordering = ('region_pk',)

    def __str__(self):
        return f"{self.name}"

# Profile 2 Model


class Profile_2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False)
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name}"

# Station model


class Station(models.Model):
    station_pk = models.AutoField(primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False, unique=True)

    class Meta:
        ordering = ('station_pk',)

    def __str__(self):
        return f"ID: {self.station_pk} - {self.name}"

# Hod model


class Hod(models.Model):
    hod_pk = models.AutoField(primary_key=True)
    hod_name = models.CharField(max_length=30, null=False)
    hod_number = models.CharField(max_length=15, null=False)
    hod_email = models.CharField(max_length=30, null=False)

    def __str__(self):
        return f"{self.hod_name} - {self.hod_number} - {self.hod_email}"

# Tickets model


class Ticket(models.Model):
    ticket_pk = models.AutoField(primary_key=True)
    ticket_number = models.CharField(max_length=30, null=False)
    ticket_officer = models.CharField(max_length=30, null=False)
    ticket_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_number} - {self.ticket_officer} - {self.ticket_date}"

# Monitor Model


class Monitor(models.Model):
    monitor_pk = models.AutoField(primary_key=True)
    monitor_serial = models.CharField(max_length=30, blank=True, default=None)
    monitor_model = models.CharField(max_length=30,  blank=True, default=None)
    monitor_tag = models.CharField(max_length=30,  blank=True, default=None)
    monitor_cpu = models.CharField(
        max_length=30, null=True, blank=True, default=None)
    cpu_assigned = models.CharField(max_length=5, default='Yes', null=False)
    date_deployed = models.DateField(auto_now_add=True)
    deployed_by = models.CharField(
        max_length=30, null=True, blank=True, default=None)
    date_changed = models.DateField(null=True, blank=True, default=None)
    reason_changed = models.CharField(
        max_length=60, null=True, blank=True, default=None)
    changed_by = models.CharField(
        max_length=30, null=True, blank=True, default=None)
    status = models.CharField(max_length=15, default='WORKING')
    ticket_number = models.CharField(
        max_length=30, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.monitor_serial}, {self.monitor_model}, {self.monitor_tag}, {self.monitor_cpu}, {self.cpu_assigned}"

# Clients Model


class Client(models.Model):
    client_pk = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=30, null=False)
    staff_number = models.CharField(max_length=15, null=False)
    staff_email = models.EmailField(null=False)
    department = models.CharField(max_length=30, null=False)
    section = models.CharField(max_length=30, null=False)
    location = models.CharField(max_length=50, null=False)
    vkey = models.CharField(max_length=50, null=False, default='vkey')
    accepted = models.CharField(max_length=10, null=False, default='Pending')
    hod_approval = models.CharField(
        max_length=10, null=False, default='Pending')
    date_assigned = models.DateField(auto_now_add=True)
    asset_serial = models.CharField(max_length=30, null=False)
    date_changed = models.DateField(null=True, blank=True, default=None)
    reason_changed = models.CharField(max_length=60, null=False, blank=True)
    changed_by = models.CharField(max_length=30, null=False, blank=True)
    hod = models.ForeignKey(Hod, null=True, blank=True,
                            default=None, on_delete=models.SET_NULL)
    assigned_by = models.CharField(max_length=30, null=False)
    ticket = models.CharField(max_length=30, null=True,
                              blank=True, default=None)
    asset_assigned = models.CharField(max_length=30, default='Yes')

    def __str__(self):
        return f"{self.full_name}, {self.staff_number}, {self.staff_email}, {self.department}, {self.section}"

# Station model


class Assettype(models.Model):
    assettype_pk = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)

    class Meta:
        ordering = ('assettype_pk',)

    def __str__(self):
        return f"ID: {self.assettype_pk} - {self.name}"

# Comp model


class Comp(models.Model):
    asset_pk = models.AutoField(primary_key=True)
    assettype = models.ForeignKey(Assettype, on_delete=models.CASCADE)
    asset_serial = models.CharField(max_length=50, null=False, unique=True)
    asset_model = models.CharField(max_length=50, null=False)
    asset_tag = models.CharField(max_length=50, blank=True, default=None)
    mac_address = models.CharField(max_length=50, null=False)
    cpu_name = models.CharField(max_length=30, blank=True, default=None)
    domain = models.CharField(max_length=5, blank=True, default=None)
    reason_no_domain = models.CharField(
        max_length=30, blank=True, default=None)
    ram = models.CharField(max_length=10, blank=True, default=None)
    os = models.CharField(max_length=15, blank=True, default=None)
    adss = models.CharField(max_length=5, blank=True, default=None)
    laps = models.CharField(max_length=5, blank=True, default=None)
    wol = models.CharField(max_length=5, blank=True, default=None)
    kaspersky = models.CharField(max_length=5, blank=True, default=None)
    reason_no_kaspersky = models.CharField(
        max_length=30, blank=True, default=None)
    ip_address = models.CharField(max_length=15, blank=True, default=None)
    extension = models.CharField(max_length=10, blank=True, default=None)
    deployed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    condition = models.CharField(max_length=20, null=False, default='Working')
    monitor = models.ForeignKey(Monitor, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    station = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL)
    ict_approval = models.CharField(
        max_length=30, null=False, default='Pending')
    reject_reason = models.CharField(
        max_length=50, null=True, blank=True, default=None)
    approved_by = models.CharField(
        max_length=40, null=True, blank=True, default=None)
    ticket = models.ForeignKey(
        Ticket, max_length=30, null=True, on_delete=models.SET_NULL)
    deployed_date = models.DateField(auto_now_add=True)
    obso_date = models.DateField(null=True, blank=True, default=None)
    obso_reason = models.CharField(
        max_length=50, null=True, blank=True, default=None)
    obso_officer = models.CharField(
        max_length=40, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.assettype.name}, {self.asset_serial}, {self.asset_model}, {self.asset_tag}, {self.condition}"

# Repair


class Repair(models.Model):
    repair_pk = models.AutoField(primary_key=True)
    cdate = models.DateField(auto_now_add=True)
    problem = models.CharField(max_length=60, null=False)
    solution = models.CharField(max_length=60,  blank=True)
    officer_assigned = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)
    ticket_number = models.CharField(max_length=30, null=False)
    status = models.CharField(max_length=20, null=True,
                              blank=True, default='Pending')
    officer_returned = models.CharField(max_length=30, blank=True)
    rdate = models.DateField(null=True, blank=True,
                             default=datetime(1900, 1, 1))
    comp = models.ForeignKey(Comp, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.cdate}, {self.ticket_number}, {self.officer_assigned.profile_2.name}, {self.officer_returned}, {self.rdate}"
