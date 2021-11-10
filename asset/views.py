from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from comp.settings import EMAIL_HOST_USER
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from .forms import *
from django.contrib import messages
from datetime import datetime, date
import secrets
from .models import *
from .communications import *
from .decorators import *
import json
import csv

# Home tab views


@login_required
@allowed_users(role='supervisor_ict')
def index(request):
    # Displaying deployed assets
    try:
        data = Comp.objects.exclude(client__staff_number="ICT").exclude(
            condition__icontains='Obsolete').all().order_by('-deployed_date')
    except:
        data = []

    if len(list(data)) > 0:
        num = data.count()
        date = datetime.today().strftime('%Y-%m-%d')

        # pagination
        page_number = request.GET.get('page', 1)
        paginator = Paginator(data, 15)  # Show 15 contacts per page.

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {

            'page_obj': page_obj, 'num': num, 'date': date
        }

        return render(request, 'asset/home/index.html', context)
    else:
        return render(request, 'asset/home/norecord.html')


@login_required
@allowed_users(role='supervisor_ict')
def result(request):
    # searching deployed assets
    if request.method == "POST":
        search = request.POST['criteria'].strip()
        entry = request.POST['entry'].strip()

        if search == 'serial-no':
            try:
                data = Comp.objects.exclude(client__staff_number="ICT").exclude(
                    condition__icontains='Obsolete').filter(asset_serial__icontains=entry).order_by('-deployed_date')
                num = data.count()
            except:
                data = []
                num = ''
            if len(list(data)) > 0 and num != 0:
                date = datetime.today().strftime('%Y-%m-%d')
                page = request.GET.get('page', 1)

                paginator = Paginator(data, 15)  # Display 15 Records
                try:
                    page_obj = paginator.page(page)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                context = {
                    # 'data': data,
                    'page_obj': page_obj,
                    'num': num,
                    'date': date,
                }
                return render(request, 'asset/home/result.html', context)
            else:
                return render(request, 'asset/home/norecord.html')

        elif search == 'user_number':
            try:
                data = Comp.objects.exclude(client__staff_number="ICT").exclude(condition__icontains='Obsolete').filter(
                    client__staff_number__icontains=entry).order_by('-deployed_date')
                num = data.count()
            except:
                data = []
                num = ''

            if len(list(data)) > 0 and num != 0:
                date = datetime.today().strftime('%Y-%m-%d')
                page = request.GET.get('page', 1)

                paginator = Paginator(data, 30)  # Display 15 Records
                try:
                    page_obj = paginator.page(page)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                context = {
                    # 'data': data,
                    'page_obj': page_obj,
                    'num': num,
                    'date': date,
                }
                return render(request, 'asset/home/result.html', context)
            else:
                return render(request, 'asset/home/norecord.html')

        elif search == 'asset_type':
            try:
                data = Comp.objects.exclude(client__staff_number="ICT").exclude(
                    condition__icontains='Obsolete').filter(assettype__name__icontains=entry).order_by('-deployed_date')
                num = data.count()

            except:
                data = []
                num = ''

            if len(list(data)) > 0 and num != 0:
                date = datetime.today().strftime('%Y-%m-%d')
                page = request.GET.get('page', 1)

                paginator = Paginator(data, 40)  # Display 15 Records
                try:
                    page_obj = paginator.page(page)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                context = {
                    # 'data': data,
                    'page_obj': page_obj,
                    'num': num,
                    'date': date,
                }
                return render(request, 'asset/home/result.html', context)
            else:
                return render(request, 'asset/home/norecord.html')

        elif search == 'location':
            try:
                data = Comp.objects.exclude(client__staff_number="ICT").exclude(
                    condition__icontains='Obsolete').filter(region__name__icontains=entry).order_by('-deployed_date')
                num = data.count()
            except:
                data = []
                num = ''

            if len(list(data)) > 0 and num != 0:
                date = datetime.today().strftime('%Y-%m-%d')
                page = request.GET.get('page', 1)

                paginator = Paginator(data, 40)  # Display 15 Records
                try:
                    page_obj = paginator.page(page)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                context = {
                    # 'data': data,
                    'page_obj': page_obj,
                    'num': num,
                    'date': date,
                }
                return render(request, 'asset/home/result.html', context)
            else:
                return render(request, 'asset/home/norecord.html')
    else:
        return HttpResponse("Invalid URL")

# Deployment tab views


@login_required
@allowed_users(role='supervisor_ict')
def live_search(request):
    # Live serial number search
    if request.method == 'POST':
        serial = json.loads(request.body).get('searchText')

        response = Comp.objects.filter(asset_serial__icontains=serial)

        data = response.values()

        return JsonResponse(list(data), safe=False)

# Load Asset Type ajax Call


@login_required
@allowed_users(role='supervisor_ict')
def load_assettype(request):

    asset_type = Assettype.objects.all()
    context = {
        'asset_type': asset_type
    }
    return render(request, 'asset/ajax/asset_type.html', context)

# Load Region ajax Call


@login_required
@allowed_users(role='supervisor_ict')
def load_region(request):
    region = Region.objects.all()
    context = {
        'region': region
    }
    return render(request, 'asset/ajax/region.html', context)


# Load Station ajax Call
@login_required
@allowed_users(role='supervisor_ict')
def load_station(request):
    id = request.GET.get('RegionId')
    station = Station.objects.filter(region__region_pk=id)
    context = {
        'station': station
    }
    return render(request, 'asset/ajax/station.html', context)


@login_required
@allowed_users(role='supervisor_ict')
def live_mac(request):
    # Live mac address search
    if request.method == 'POST':
        serial = json.loads(request.body).get('searchText')

        response = Comp.objects.filter(mac_address__icontains=serial)

        data = response.values()

        return JsonResponse(list(data), safe=False)


@login_required
@allowed_users(role='supervisor_ict')
def old(request):
    # processing form data
    if request.method == "POST":
        # comp data
        vkey = secrets.token_hex(15)
        officer = request.user
        ty = int(request.POST['type'])
        ty = Assettype.objects.get(assettype_pk=ty)
        serial = request.POST['sno'].strip().upper()
        model = request.POST['assetmodel'].strip().upper()
        assettag = request.POST['assettag'].strip().upper()
        monitormodel = request.POST['monitormodel'].strip().upper()
        monitorserial = request.POST['monitorserial'].strip().upper()
        monitortag = request.POST['monitortag'].strip().upper()
        no_kas = request.POST['no_kaspersky'].strip()
        domain = request.POST['domain'].strip()
        laps = request.POST['laps'].strip()
        adss = request.POST['adss'].strip()
        kasper = request.POST['kaspeski'].strip()
        wol = request.POST['WOL'].strip()
        mac = request.POST['macaddress'].strip().upper()
        compname = request.POST['compname'].strip().upper()
        os = request.POST['os'].strip().upper()
        reason_no_domain = request.POST['no_domain'].strip()
        ram = request.POST['ram'].strip()
        ip_address = request.POST['ip'].strip()
        extension = request.POST['extension'].strip()

        # work ticket details
        ticket = request.POST['ticket'].strip().upper()
        officer_t = request.POST['officer'].strip().upper()
        ticket_date = request.POST['ticket_date'].strip()

        # Staff details
        full_name = request.POST['cowner'].strip().upper()
        pno = request.POST['employeeno'].strip().upper()
        email = request.POST['emailno'].strip().upper()
        location = request.POST['clocation'].strip().upper()
        dept = request.POST['dept'].strip().upper()
        section = request.POST['section'].strip().upper()
        region = int(request.POST['region'])
        region = Region.objects.get(region_pk=region)
        station = int(request.POST['station'])
        station = Station.objects.get(station_pk=station)

        # Hod
        hod_name = request.POST['hod'].strip().upper()
        hod_number = request.POST['hod_no'].strip().upper()
        hod_email = request.POST['hod_email'].strip().upper()

        # checking if serial number already captured
        if Comp.objects.filter(asset_serial=serial).count() < 1:
            # checking if hod exists
            if Hod.objects.filter(hod_number__icontains=hod_number).count() < 1:
                # # insert into region
                # r = Region(regional=region,station=station,location=location)
                # r.save()
                # insert into hod
                h = Hod(hod_name=hod_name, hod_number=hod_number,
                        hod_email=hod_email)
                h.save()
                # insert into ticket
                t = Ticket(ticket_number=ticket, ticket_officer=officer_t)
                t.save()
                # insert into monitors
                # Check if desktop
                if ty.name == 'DESKTOP/LAPTOP':
                    m = Monitor(monitor_serial=monitorserial, monitor_model=monitormodel,
                                monitor_tag=monitortag, monitor_cpu=serial, deployed_by=officer,)
                    m.save()
                else:
                    m = Monitor.objects.get(monitor_pk=1)
                # insert into clients
                c = Client(full_name=full_name, staff_number=pno, staff_email=email, department=dept, section=section,
                           asset_serial=serial, assigned_by=officer, ticket=ticket, hod=h, vkey=vkey, location=location)
                c.save()
                # insert into comp
                comp = Comp(assettype=ty, asset_serial=serial, asset_model=model, asset_tag=assettag, mac_address=mac, cpu_name=compname, domain=domain, reason_no_domain=reason_no_domain, ram=ram, os=os, adss=adss,
                            laps=laps, wol=wol, kaspersky=kasper, reason_no_kaspersky=no_kas, ip_address=ip_address, extension=extension, deployed_by=officer, monitor=m, client=c, region=region, station=station, ticket=t)
                comp.save()
                # Send email, Flash message and redirect to home page

                email_hod(serial)
                messages.success(request, f"Record inserted successfully!!!")
                return redirect('home')
            else:
                # get hod id and continue inserting
                hod_id = Hod.objects.filter(
                    hod_number__icontains=hod_number).first()

                # # insert into region
                # r = Region(regional=region,station=station,location=location)
                # r.save()
                # insert into ticket
                t = Ticket(ticket_number=ticket, ticket_officer=officer_t)
                t.save()

                # insert into monitors
                # Check if Desktop
                if ty.name == 'DESKTOP/LAPTOP':
                    m = Monitor(monitor_serial=monitorserial, monitor_model=monitormodel,
                                monitor_tag=monitortag, monitor_cpu=serial, deployed_by=officer,)
                    m.save()
                else:
                    m = Monitor.objects.get(monitor_pk=1)
                # insert into clients
                c = Client(full_name=full_name, staff_number=pno, staff_email=email, department=dept, section=section,
                           asset_serial=serial, assigned_by=officer, ticket=ticket, hod=hod_id, vkey=vkey, location=location)
                c.save()
                # insert into comp
                comp = Comp(assettype=ty, asset_serial=serial, asset_model=model, asset_tag=assettag, mac_address=mac, cpu_name=compname, domain=domain, reason_no_domain=reason_no_domain, ram=ram, os=os, adss=adss,
                            laps=laps, wol=wol, kaspersky=kasper, reason_no_kaspersky=no_kas, ip_address=ip_address, extension=extension, deployed_by=officer, monitor=m, client=c, region=region, station=station, ticket=t)
                comp.save()
                # Send email, Flash message and redirect to home page

                try:
                    email_hod(serial)
                    messages.success(
                        request, f"Asset Record captured successfully!!!")
                    return redirect('home')
                except:
                    messages.success(
                        request, f"Asset Record captured successfully!!!")
                    return redirect('home')
        else:
            # Flash message and redirect to home page
            messages.info(
                request, f"Asset serial number already Registered!!!")
            return redirect('deployment_old')
    else:
        return render(request, 'asset/deployment/old.html')


def client_accept(request):
    if request.method == 'GET':
        vkey = request.GET['vkey'].strip()
        serial = request.GET['serial'].strip()

        if Client.objects.get(comp__asset_serial=serial, vkey=vkey).accepted == 'Pending':
            Client.objects.filter(comp__asset_serial=serial, vkey=vkey).update(
                accepted='Accepted')

            try:
                email_ict(serial)
                return render(request, 'asset/mail/accept.html')
            except:
                return render(request, 'asset/mail/accept.html')
        else:
            return render(request, 'asset/mail/accept1.html')


def hod_accept(request):
    if request.method == 'GET':
        vkey = request.GET['vkey'].strip()
        serial = request.GET['serial'].strip()

        if Client.objects.get(comp__asset_serial=serial, vkey=vkey).hod_approval == 'Pending':
            Client.objects.filter(comp__asset_serial=serial, vkey=vkey).update(
                hod_approval='Approved')

            try:
                email_client(serial)
                email_deliver(serial)
                return render(request, 'asset/mail/hod_accept.html')
            except:
                return render(request, 'asset/mail/hod_accept.html')
        else:
            return render(request, 'asset/mail/hod_accept1.html')


@login_required
@allowed_users(role='supervisor_ict')
def new(request):
    return render(request, 'asset/deployment/new.html')


@login_required
@allowed_users(role='supervisor_ict')
def batch(request):
    return render(request, 'asset/deployment/batch.html')


# Data Approval tab
@login_required
@allowed_users(role='supervisor_ict')
def approve(request):
    try:
        data = Comp.objects.filter(ict_approval='Pending').order_by(
            '-client__date_assigned', 'assettype')
        num = data.count()
    except:
        data = []
        num = ''

    if len(list(data)) > 0 and num != 0:
        date = datetime.today().strftime('%Y-%m-%d')
        # Pagination
        page = request.GET.get('page', 1)

        paginator = Paginator(data, 15)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'page_obj': page_obj,
            'num': num,
            'date': date
        }
        return render(request, 'asset/approval/approve.html', context)
    else:
        return render(request, 'asset/approval/norecordhome.html')


@login_required
@allowed_users(role='supervisor_ict')
def approveresult(request):
    # displaying deployment report
    if request.method == "POST":
        serial = request.POST['entry'].strip()
        try:
            data = Comp.objects.get(
                asset_serial__icontains=serial, ict_approval='Pending')
        except:
            data = ''

        if data != '':

            context = {
                'data': data,
            }

            return render(request, 'asset/approval/approveresult.html', context)
        else:
            return render(request, 'asset/approval/norecord.html')

    if request.method == 'GET':
        id = request.GET['id']
        data = Comp.objects.get(asset_serial=id)

        context = {
            'data': data
        }
        return render(request, 'asset/approval/approveresult.html', context)


@login_required
@allowed_users(role='supervisor_ict')
@allowed_admin(role='admin_ict')
def ict_approve(request):
    # Ict admin approves asset deployment
    if request.method == 'GET':
        id = request.GET['id']

        # check if user accepted the asset
        if Comp.objects.get(asset_serial=id).client.accepted == 'Accepted':
            # check if hod approved deployment
            if Comp.objects.get(asset_serial=id).client.hod_approval == 'Approved':
                # check if record already approved
                if Comp.objects.get(asset_serial=id).ict_approval == 'Approved':
                    # Flash message
                    messages.info(
                        request, f"Asset Already Approved by ICT Admin!!!")
                    return redirect('approve')
                else:
                    # update comp table
                    officer = request.user.profile_2.name
                    data = Comp.objects.filter(asset_serial=id)
                    data.update(ict_approval='Approved')
                    data.update(approved_by=officer)

                    # send email, Flash message and redirect to home page
                    try:
                        email_approve(id)
                        messages.success(
                            request, f"Asset approved successfully!!!")
                        return redirect('approve')
                    except:
                        messages.success(
                            request, f"Asset approved successfully, but did not send final deployment report!!!")
                        return redirect('approve')
            else:
                # Flash message and redirect to home page
                messages.info(
                    request, f"Asset not Approved by HOD/Supervisor!!!")
                return redirect('approve')
        else:
            # Flash message and redirect to home page
            messages.info(request, f"Asset not Accepted by user!!!")
            return redirect('approve')


@login_required
@allowed_users(role='supervisor_ict')
@allowed_admin(role='admin_ict')
def ict_reject(request):
    if request.method == 'POST':
        id = request.POST['id'].strip()
        reject = request.POST['reject'].strip()
        # check if already approved
        if Comp.objects.get(asset_serial=id).ict_approval == 'Approved' or Comp.objects.get(asset_serial=id).ict_approval == 'Rejected':
            # Flash message
            messages.info(
                request, f"Asset Already Approved/Rejected by ICT Admin!!!")
            return redirect('approve')
        else:
            officer = request.user.first_name
            data = Comp.objects.filter(asset_serial=id)
            data.update(reject_reason=reject)
            data.update(ict_approval='Rejected')
            data.update(approved_by=officer)
            messages.success(request, f"Asset Updated successfully!!!")
            return redirect('approve')

# Asset Edit


@login_required
@allowed_users(role='supervisor_ict')
@allowed_admin(role='admin_ict')
# @allowed_users(allowed_roles = ['admin_ict'])
def edit_home(request):
    # home view
    try:
        data = Comp.objects.filter(ict_approval__icontains='Rejected').order_by(
            '-client__date_assigned')
        num = data.count()
    except:
        data = []
        num = ''

    if len(list(data)) > 0 and num != 0:
        date = datetime.today().strftime('%Y-%m-%d')
        page = request.GET.get('page', 1)

        paginator = Paginator(data, 15)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'page_obj': page_obj,
            'num': num,
            'date': date
        }
        return render(request, 'asset/edit/home.html', context)
    else:
        return render(request, 'asset/edit/norecord.html')


@login_required
@allowed_users(role='supervisor_ict')
def edit_view(request):
    # Edit view
    if request.method == 'POST':
        id = request.POST['entry'].strip()

        try:
            data = Comp.objects.get(asset_serial=id)
        except:
            data = ''

        if data != '':
            context = {
                'data': data,
            }
            return render(request, 'asset/edit/edit.html', context)
        else:
            return render(request, 'asset/edit/norecord.html')

    if request.method == 'GET':
        id = request.GET['id']
        data = Comp.objects.get(asset_serial=id)

        context = {
            'data': data
        }
        return render(request, 'asset/edit/edit.html', context)


@login_required
@allowed_users(role='supervisor_ict')
def edit_back(request):
    # Edit backend
    if request.method == 'POST':
        asset_id = request.POST['asset_id']
        client_id = request.POST['client_id']
        ty = request.POST['type'].strip().upper()
        serial = request.POST['sno'].strip().upper()
        model = request.POST['assetmodel'].strip().upper()
        assettag = request.POST['assettag'].strip().upper()
        monitormodel = request.POST['monitormodel'].strip().upper()
        monitorserial = request.POST['monitorserial'].strip().upper()
        monitortag = request.POST['monitortag'].strip().upper()
        no_kas = request.POST['no_kaspersky'].strip().upper()
        domain = request.POST['domain'].strip().upper()
        laps = request.POST['laps'].strip().upper()
        adss = request.POST['adss'].strip().upper()
        kasper = request.POST['kaspeski'].strip().upper()
        wol = request.POST['WOL'].strip().upper()
        mac = request.POST['macaddress'].strip().upper()
        compname = request.POST['compname'].strip().upper()
        os = request.POST['os'].strip().upper()
        reason_no_domain = request.POST['no_domain'].strip().upper()
        ram = request.POST['ram'].strip().upper()
        ip_address = request.POST['ip'].strip().upper()
        extension = request.POST['extension'].strip().upper()

        # Staff details
        full_name = request.POST['cowner'].strip().upper()
        pno = request.POST['employeeno'].strip().upper()
        email = request.POST['emailno'].strip().upper()
        location = request.POST['clocation'].strip().upper()
        dept = request.POST['dept'].strip().upper()
        section = request.POST['section'].strip().upper()
        region = request.POST['region'].strip().upper()
        station = request.POST['station'].strip().upper()

        # Hod
        hod_name = request.POST['hod'].strip().upper()
        hod_number = request.POST['hod_no'].strip().upper()
        hod_email = request.POST['hod_email'].strip().upper()

        # Get asset with that serial number
        asset = Comp.objects.filter(asset_pk__icontains=asset_id)

        # Update the asset record
        # Asset
        asset.update(asset_model=model, asset_tag=assettag, reason_no_kaspersky=no_kas, domain=domain, laps=laps, adss=adss, kaspersky=kasper, wol=wol, mac_address=mac,
                     cpu_name=compname, os=os, reason_no_domain=reason_no_domain, ram=ram, ip_address=ip_address, extension=extension, ict_approval='Approved', reject_reason='')

        # Staff details
        Client.objects.filter(comp__asset_pk=asset_id).update(
            full_name=full_name)
        Client.objects.filter(comp__asset_pk=asset_id).update(staff_number=pno)
        Client.objects.filter(
            comp__asset_pk=asset_id).update(staff_email=email)
        Client.objects.filter(comp__asset_pk=asset_id).update(department=dept)
        Client.objects.filter(comp__asset_pk=asset_id).update(section=section)
        Client.objects.filter(comp__asset_pk=asset_id).update(
            asset_serial=serial)
        # Region details
        Region.objects.filter(comp__asset_pk=asset_id).update(regional=region)
        Region.objects.filter(comp__asset_pk=asset_id).update(station=station)
        Region.objects.filter(
            comp__asset_pk=asset_id).update(location=location)
        # Hod Details
        Hod.objects.filter(client__client_pk=client_id).update(
            hod_name=hod_name)
        Hod.objects.filter(client__client_pk=client_id).update(
            hod_number=hod_number)
        Hod.objects.filter(client__client_pk=client_id).update(
            hod_email=hod_email)

        # Flash Message
        messages.success(request, f"Asset Record edited Successfully!!!")

        # Redirect
        return redirect('asset_edit')


# Asset Relocation
@login_required
@allowed_users(role='supervisor_ict')
def relocate(request):
    if request.method == 'GET':
        return render(request, 'asset/relocate/relocate.html')
    else:
        return HttpResponse("Invalid HTTP METHOD")


@login_required
@allowed_users(role='supervisor_ict')
def rel(request):
    # Get form data
    if request.method == 'POST':
        asset_serial = request.POST['entry'].strip()
        try:
            data = Comp.objects.get(asset_serial__icontains=asset_serial)
        except:
            data = ''

        if data != '':
            context = {
                'data': data
            }

            return render(request, 'asset/relocate/rel.html', context)
        else:
            return render(request, 'asset/relocate/norecord.html')
    else:
        return HttpResponse("Invalid HTTP METHOD")


@login_required
@allowed_users(role='supervisor_ict')
def rel_back(request):
    if request.method == 'POST':
        id = request.POST['serial'].strip()
        dept = request.POST['dept'].strip().upper()
        section = request.POST['section'].strip().upper()
        region = int(request.POST['region'])
        region = Region.objects.get(region_pk=region)
        station = int(request.POST['station'])
        station = Station.objects.get(station_pk=station)
        location = request.POST['location'].strip().upper()
        hod_no = request.POST['hod_no'].strip().upper()
        hod_name = request.POST['hod_name'].strip().upper()
        hod_email = request.POST['hod_email'].strip().upper()

        # checking if approved by ICT admin
        if Comp.objects.get(asset_serial=id).ict_approval == 'Approved':
            # checking if HOD exists
            if Hod.objects.filter(hod_number__icontains=hod_no).count() > 0:
                h = Hod.objects.filter(hod_number=hod_no).first()
                c = Client.objects.filter(comp__asset_serial=id)
                c.update(department=dept)
                c.update(section=section)
                c.update(location=location)
                c.update(hod=h)
                comp = Comp.objects.filter(asset_serial=id)
                comp.update(region=region)
                comp.update(station=station)

                # Send mail and flash message
                try:
                    asset_relocate(id)
                    messages.success(
                        request, f"Asset Relocated successfully!!!")
                    return redirect('relocate')
                except:
                    messages.info(
                        request, f"Asset Relocated successfully, but email not send!!!")
                    return redirect('relocate')

            else:
                # insert record
                h = Hod(hod_name=hod_name, hod_number=hod_no,
                        hod_email=hod_email)
                h.save()
                c = Client.objects.filter(comp__asset_serial=id)
                c.update(department=dept)
                c.update(section=section)
                c.update(location=location)
                c.update(hod=h)
                comp = Comp.objects.filter(asset_serial=id)
                comp.update(region=region)
                comp.update(station=station)

                # Send mail and flash message
                try:
                    asset_relocate(id)
                    messages.info(request, f"Record updated successfully!!!")
                    return redirect('relocate')
                except:
                    messages.info(
                        request, f"Asset Relocated successfully, but email not send!!!")
                    return redirect('relocate')

        else:
            messages.info(
                request, f"Record not approved or rejected by ICT Admin")
            return redirect('relocate')
    else:
        return HttpResponse("Invalid HTTP METHOD")


# Replace monitor


@login_required
@allowed_users(role='supervisor_ict')
def monitor(request):
    if request.method == 'GET':
        return render(request, 'asset/monitor/monitor.html')
    else:
        return HttpResponse("Invalid HTTP METHOD")


@login_required
@allowed_users(role='supervisor_ict')
def details(request):
    # display current monitor details
    if request.method == 'POST':
        officer = request.user.first_name
        id = request.POST['entry'].strip()

        try:
            data = Comp.objects.get(
                asset_serial__icontains=id, assettype__name__icontains='DESKTOP')
        except:
            data = ''

        if data != '':

            context = {
                'data': data
            }
            return render(request, 'asset/monitor/details.html', context)
        else:
            return render(request, 'asset/monitor/norecord.html')
    else:
        return HttpResponse("Invalid HTTP METHOD")


@login_required
@allowed_users(role='supervisor_ict')
def monitor_change(request):
    if request.method == 'POST':
        officer = request.user.username
        id = request.POST['id'].strip()
        condition = request.POST['condition'].strip()
        model = request.POST['model'].strip()
        serial = request.POST['serial'].strip()
        tag = request.POST['tag'].strip()
        reason = request.POST['reason'].strip()

        # getting id of old monitor
        mon_id = Monitor.objects.get(comp__asset_serial=id).monitor_pk

        # Checking asset approved by ICT Admin
        if Comp.objects.get(asset_serial=id).ict_approval == 'Approved' and Monitor.objects.get(comp__asset_serial=id).monitor_serial != serial:
            # insert monitor record
            m = Monitor(monitor_serial=serial, monitor_model=model,
                        monitor_tag=tag, deployed_by=officer, monitor_cpu=id)
            m.save()
            # Update Comp table
            Comp.objects.filter(asset_serial=id).update(monitor=m)
            # Update old monitor record
            date = datetime.today().strftime('%Y-%m-%d')
            M = Monitor.objects.filter(monitor_pk=mon_id)
            M.update(cpu_assigned='NO')
            M.update(status=condition)
            M.update(changed_by=officer)
            M.update(reason_changed=reason)
            M.update(date_changed=date)
            # Send mail and flash message
            try:
                replace_monitor(id)
                messages.success(request, f"Replaced monitor successfully!!!")
                return redirect('monitor')
            except:
                messages.success(
                    request, f"Replaced monitor successfully, but did not send email to the user!!!")
                return redirect('monitor')
        else:
            messages.info(
                request, f"Record not Approved by ICT Admin Or Already Assigned to a User!!")
            return redirect('monitor')
    else:
        return HttpResponse("Invalid HTTPP METHOD")

# Change ownership


@login_required
@allowed_users(role='supervisor_ict')
def search(request):
    if request.method == 'GET':
        return render(request, 'asset/ownership/search.html')
    else:
        return HttpResponse("Invalid HTTPP METHOD")


@login_required
@allowed_users(role='supervisor_ict')
def change(request):
    if request.method == 'POST':
        serial = request.POST['entry'].strip()
        # Query database
        try:
            data = Comp.objects.get(asset_serial__icontains=serial)
        except:
            data = ''

        context = {
            'data': data,
        }

        if data != '':
            return render(request, 'asset/ownership/change.html', context)
        else:
            return render(request, 'asset/ownership/norecord.html')
    else:
        return HttpResponse("Invalid HTTPP METHOD")


@login_required
@allowed_users(role='supervisor_ict')
def change_back(request):
    # Change of ownership
    if request.method == 'POST':
        asset_pk = request.POST['asset_pk']
        asset_serial = request.POST['asset_serial'].strip()
        owner_pk = request.POST['owner_pk']
        name = request.POST['owner'].strip().upper()
        number = request.POST['number'].strip().upper()
        email = request.POST['email'].strip().upper()
        location = request.POST['location'].strip().upper()
        dept = request.POST['dept'].strip().upper()
        section = request.POST['section'].strip().upper()
        region = int(request.POST['region'])
        region = Region.objects.get(region_pk=region)
        station = int(request.POST['station'])
        station = Station.objects.get(station_pk=station)
        reason = request.POST['reason'].strip().upper()
        hod_pk = request.POST['hod_pk']
        hod_name = request.POST['hod_name'].strip().upper()
        hod_no = request.POST['hod_no'].strip().upper()
        hod_email = request.POST['hod_email'].strip().upper()
        officer = request.user.profile_2.name
        date = datetime.today().strftime('%Y-%m-%d')

        # Check if ICT asset deployment approved by ICT Admin
        if Comp.objects.get(asset_serial__icontains=asset_serial).ict_approval == 'Approved':
            # Check if HOD already exists
            if Hod.objects.filter(hod_number__icontains=hod_no).count() > 0:
                # get hod pk
                h = Hod.objects.filter(hod_number__icontains=hod_no).first()

                # Save new owner
                c = Client(full_name=name, staff_number=number, staff_email=email, department=dept, section=section, assigned_by=officer, hod=h, location=location,
                           asset_serial=asset_serial, accepted="Accepted", hod_approval="Approved")
                c.save()
                # Update Comp table
                comp = Comp.objects.filter(asset_pk=asset_pk)
                comp.update(client=c)
                comp.update(region=region)
                comp.update(station=station)

                # update old owner
                client = Client.objects.filter(client_pk=owner_pk)
                client.update(date_changed=date)
                client.update(reason_changed=reason)
                client.update(changed_by=officer)
                client.update(asset_assigned='No')

                # send mail and Flash message
                try:
                    change_asset_ownership(asset_serial, owner_pk)
                    messages.info(
                        request, f"Asset Changed ownership successfully!!!")
                    return redirect('ownership_search')
                except:
                    messages.info(
                        request, f"Asset Changed ownership successfully, but email not send to user!!!")
                    return redirect('ownership_search')
            else:
                # Save hod details
                h = Hod(hod_name=hod_name, hod_number=hod_no,
                        hod_email=hod_email)
                h.save()

                # Save new owner
                c = Client(full_name=name, staff_number=number, staff_email=email, department=dept, section=section, assigned_by=officer, hod=h, location=location,
                           asset_serial=asset_serial, accepted="Accepted", hod_approval="Approved")
                c.save()

                # Update Comp table
                comp = Comp.objects.filter(asset_pk=asset_pk)
                comp.update(client=c)
                comp.update(region=region)
                comp.update(station=station)

                # update old owner
                client = Client.objects.filter(client_pk=owner_pk)
                client.update(date_changed=date)
                client.update(reason_changed=reason)
                client.update(changed_by=officer)
                client.update(asset_assigned='No')

                # Flash message
                try:
                    change_asset_ownership(asset_serial, owner_pk)
                    messages.info(
                        request, f"Asset Changed ownership successfully!!!")
                    return redirect('ownership_search')
                except:
                    messages.info(
                        request, f"Asset Changed ownership successfully, but email not send to user!!!")
                    return redirect('ownership_search')
        else:
            messages.info(
                request, f"Asset Record not Approved by ICT Admin!!!")
            return redirect('ownership_search')
    else:
        return HttpResponse("Invalid HTTP METHOD")

# Surrender Asset


@login_required
@allowed_users(role='supervisor_ict')
def surrender(request):
    return render(request, 'asset/surrender/surrender.html')


@login_required
@allowed_users(role='supervisor_ict')
def surrenderback(request):
    if request.method == 'POST':
        id = request.POST['entry'].strip()

        try:
            data = Comp.objects.exclude(client__staff_number="ICT").get(
                asset_serial__icontains=id)
        except:
            data = ''

        if data != '':
            context = {
                'data': data
            }
            return render(request, 'asset/surrender/surrenderback.html', context)
        else:
            return render(request, 'asset/surrender/norecord.html')
    else:
        return HttpResponse("Invalid URL")


@login_required
@allowed_users(role='supervisor_ict')
def sur_backend(request):
    if request.method == 'POST':
        id = request.POST['serial']
        client = request.POST['client']
        condition = request.POST['condition'].strip()
        reason = request.POST['reason'].strip().upper()

        # Check if approved by ICT and not already surrender
        if Comp.objects.get(asset_serial__icontains=id).ict_approval == 'Approved':
            # Insert record with user and p/no ICT
            officer = request.user.profile_2.name
            c = Client(full_name='ICT', staff_number='ICT', staff_email='ictmsa43@gmail.com', department='ICT',
                       section='ICT', asset_serial=id, assigned_by=officer, accepted="Accepted", hod_approval="Approved")

            c.save()
            # update Comp table
            Comp.objects.filter(asset_serial=id).update(client=c)
            # Update clients old record
            date = datetime.today().strftime('%Y-%m-%d')
            c = Client.objects.filter(client_pk=client)
            c.update(asset_assigned='No')
            c.update(changed_by=officer)
            c.update(reason_changed=reason)
            c.update(date_changed=date)

            # Send email and flash message
            try:
                surrender_asset(id, client)
                messages.success(request, f"Asset Surrendered Successfully!!!")
                return redirect('surrender')
            except:
                messages.success(
                    request, f"Asset Surrendered Successfully, but did not send email to the user!!!")
                return redirect('surrender')
        else:
            messages.success(request, f"Record Not Approved by ICT Admin")
            return redirect('surrender')
    else:
        return HttpResponse("Invalid URL")


# Declare Asset Obsolete
@login_required
@allowed_users(role='supervisor_ict')
def obso(request):
    return render(request, 'asset/obsolete/obso.html')


@login_required
@allowed_users(role='supervisor_ict')
def obsoback(request):
    if request.method == 'POST':
        id = request.POST['entry']

        try:
            data = Comp.objects.exclude(condition="Obsolete").get(
                asset_serial__icontains=id, client__staff_number="ICT")
        except:
            data = ''

        if data != '':
            context = {
                'data': data
            }
            return render(request, 'asset/obsolete/obsoback.html', context)
        else:
            return render(request, 'asset/obsolete/norecord.html')
    else:
        return HttpResponse("Invalid URL")


@login_required
@allowed_users(role='supervisor_ict')
def obso_backend(request):
    if request.method == 'POST':
        id = request.POST['serial']
        reason = request.POST['reason']
        officer = request.user.profile_2.name
        date = datetime.today().strftime('%Y-%m-%d')

        # checking asset already surrendered
        if Client.objects.get(comp__asset_serial=id).staff_number == 'ICT' and Comp.objects.get(asset_serial=id).condition == 'Working':
            # update comp table
            c = Comp.objects.filter(asset_serial=id)
            c.update(condition='Obsolete')
            c.update(obso_date=date)
            c.update(obso_reason=reason)
            c.update(obso_officer=officer)
            messages.info(request, f"Asset updated successfully!!!")
            return redirect('obsolete')
        else:
            messages.info(
                request, f"Asset not surrendered or already declared obsolete!!!")
            return redirect('obsolete')
    else:
        return HttpResponse("Invalid URL")

# Asset Repairs


@login_required
@allowed_users(role='supervisor_ict')
def repairs(request):
    # Getting repair data from the database
    try:
        data = Repair.objects.exclude(
            status__icontains="solved").all().order_by('-cdate')
    except:
        data = []

    if len(list(data)) > 0:
        # pagination
        page = request.GET.get('page', 1)

        paginator = Paginator(data, 15)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'page_obj': page_obj
        }

        return render(request, 'asset/asset_repairs/repair.html', context)
    else:
        return render(request, 'asset/asset_repairs/norecord.html')


@login_required
@allowed_users(role='supervisor_ict')
def result_repairs(request):
    if request.method == 'POST':
        criteria = request.POST['criteria']
        id = request.POST['entry'].strip()

        # Get data from database
        if criteria == 'serial':
            try:
                data = Repair.objects.filter(
                    comp__asset_serial__icontains=id).order_by('-cdate')
            except:
                data = []

            if len(list(data)) > 0:
                page = request.GET.get('page', 1)

                paginator = Paginator(data, 15)
                try:
                    page_obj = paginator.page(page)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)

                context = {
                    'page_obj': page_obj,

                }

                return render(request, 'asset/asset_repairs/result.html', context)
            else:
                return render(request, 'asset/asset_repairs/norecord.html')

        elif criteria == 'number':
            try:
                data = Repair.objects.filter(
                    comp__client__staff_number=id).order_by('-cdate')
            except:
                data = []

            if len(list(data)) > 0:
                context = {
                    'data': data
                }

                return render(request, 'asset/asset_repairs/result.html', context)
            else:
                return render(request, 'asset/asset_repairs/norecord.html')
    else:
        return HttpResponse("Invalid URL")


@login_required
@allowed_users(role='supervisor_ict')
def repair_register(request):
    if request.method == 'POST':
        # Getting form data
        officer = request.user
        date = datetime.today().strftime('%Y-%m-%d')
        serial = request.POST['serail'].strip()
        problem = request.POST['problem'].strip()
        staff_number = request.POST['employeeno'].strip()
        ticket = request.POST['ticket'].strip()

        # Checking if asset exists in database
        if Comp.objects.filter(asset_serial__icontains=serial).count() > 0:
            # check if the staff is assigned that asset
            if Comp.objects.filter(asset_serial__icontains=serial, client__staff_number__icontains=staff_number).count() > 0:

                # Get staff details
                c = Comp.objects.get(
                    asset_serial__icontains=serial, client__staff_number__icontains=staff_number)

                name = c.client.full_name
                number = c.client.staff_number
                hardware = c.assettype.name
                address = c.client.staff_email

                # send mail
                context = {
                    'name': name, 'number': number, 'hardware': hardware, 'serial': serial, 'problem': problem, 'date': date, 'officer': officer.profile_2.name
                }
                subject = 'ASSET REPAIR' + ' - ' + ' INCOMING' + \
                    ' ' + ' - ' + name + ' ' + ' - ' + date
                html_message = render_to_string(
                    'asset/mail/repair_register.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'ictmsa43@gmail.com'
                to = address

                try:
                    send_mail(subject, plain_message, from_email,
                              [to], html_message=html_message)

                    # Insert the record in the database
                    comp_id = Comp.objects.get(asset_serial__icontains=serial)
                    # Saving form data to the database
                    t = Repair(problem=problem, ticket_number=ticket,
                               officer_assigned=officer, comp=comp_id)
                    t.save()

                    # Flash message and redirect to home page
                    messages.success(
                        request, f"Asset Repair captured successfully!!")
                    return redirect('asset_repairs')

                except:
                    # Insert the record in the database
                    comp_id = Comp.objects.get(asset_serial__icontains=serial)
                    # Saving form data to the database
                    t = Repair(problem=problem, ticket_number=ticket,
                               officer_assigned=officer, comp=comp_id)
                    t.save()
                    # Flash message and redirect to home page
                    messages.success(
                        request, f"Asset Repair captured successfully, But email not Sent!!!")
                    return redirect('asset_repairs')
            else:
                # Flash message
                messages.success(
                    request, f"This Asset is not assigned to this user, confirm serial number and staff number!!!")
                return redirect('asset_repairs')

        else:
            # Flash message
            messages.success(
                request, f"No such Asset in the database, check the serial number and try again!!!")
            return redirect('asset_repairs')
    else:
        return HttpResponse("Invalid URL")


@login_required
@allowed_users(role='supervisor_ict')
def repair_release(request):
    # get asset serial number
    if request.method == 'GET':
        id = request.GET['id'].strip()
        data = Repair.objects.get(repair_pk=id)

        context = {
            'data': data
        }
        return render(request, 'asset/asset_repairs/outgoing.html', context)


@login_required
@allowed_users(role='supervisor_ict')
def return_repair(request):
    if request.method == 'POST':
        officer = request.user.profile_2.name
        id = request.POST['id'].strip()
        solution = request.POST['solution'].strip()
        rdate = datetime.today().strftime('%Y-%m-%d')
        status = 'SOLVED'

        # cHECKING IF ASSET ALREADY REPAIRED
        if Repair.objects.get(repair_pk=id).status != 'SOLVED':
            # Get staff details
            c = Comp.objects.get(repair__repair_pk=id)
            r = Repair.objects.get(repair_pk=id)

            name = c.client.full_name
            number = c.client.staff_number
            hardware = c.assettype.name
            serial = c.asset_serial
            problem = r.problem
            idate = r.cdate
            collect_officer = r.officer_assigned.profile_2.name
            address = c.client.staff_email

            # send mail
            context = {
                'name': name, 'number': number, 'hardware': hardware, 'serial': serial, 'problem': problem, 'rdate': rdate, 'idate': idate, 'collect_officer': collect_officer, 'solution': solution,
                'officer': officer
            }
            subject = 'ASSET REPAIR' + ' - ' + ' OUTGOING' + \
                ' ' + ' - ' + name + ' ' + ' - ' + rdate
            html_message = render_to_string(
                'asset/mail/repair_realise.html', context)
            plain_message = strip_tags(html_message)
            from_email = 'ictmsa43@gmail.com'
            to = address

            try:
                # send mail and update record
                send_mail(subject, plain_message, from_email,
                          [to], html_message=html_message)

                data = Repair.objects.filter(repair_pk=id)
                data.update(solution=solution)
                data.update(rdate=rdate)
                data.update(status=status)
                data.update(officer_returned=officer)
                # Flash message
                messages.success(
                    request, f"Repair Record updated successfully!!!")
                return redirect('asset_repairs')
            except:
                data = Repair.objects.filter(repair_pk=id)
                data.update(solution=solution)
                data.update(rdate=rdate)
                data.update(status=status)
                data.update(officer_returned=officer)
                # Flash message and redirect to home page
                messages.success(
                    request, f"Repair Record updated successfully, But email not sent!!!")
                return redirect('asset_repairs')
        else:
            # Flash message
            messages.success(request, f"Asset Already Repaired!!!")
            return redirect('asset_repairs')
    else:
        return HttpResponse("Invalid URL")

# Deployment_report


@login_required
@allowed_users(role='supervisor_ict')
def deploy_report(request):
    return render(request, 'asset/deploy_report/approve.html')


@login_required
@allowed_users(role='supervisor_ict')
def deploy_result(request):
    if request.method == 'POST':
        id = request.POST['entry']
        date = datetime.today().strftime('%Y-%m-%d')
        try:
            data = Comp.objects.get(asset_serial__icontains=id)
        except:
            data = ''

        if data != '':
            context = {
                'data': data,
                'date': date,
            }
            return render(request, 'asset/deploy_report/report.html', context)
        else:
            return render(request, 'asset/deploy_report/norecord.html')
    else:
        return HttpResponse("Invalid URL")

# User Assets


@login_required
@allowed_users(role='supervisor_ict')
def user(request):
    return render(request, 'asset/user_assets/asset.html')


@login_required
@allowed_users(role='supervisor_ict')
def user_report(request):
    if request.method == 'POST':
        client_number = request.POST['entry'].strip()
        date = datetime.today().strftime('%Y-%m-%d')
        # get user details
        try:
            data = Comp.objects.filter(client__staff_number__icontains=client_number,
                                       client__asset_assigned='Yes')[:1]

            dat = Comp.objects.filter(client__staff_number__icontains=client_number,
                                      client__asset_assigned='Yes')
        except:
            data = ""

            dat = ""

        if len(list(data)) > 0 and len(list(dat)) > 0:
            context = {
                'data': data,
                'dat': dat,
                'date': date,
            }
            return render(request, 'asset/user_assets/report.html', context)
        else:
            return render(request, 'asset/user_assets/norecord.html')
    else:
        return HttpResponse("Invalid URL")

# Asset ownership history


@login_required
@allowed_users(role='supervisor_ict')
def history(request):
    return render(request, 'asset/owner_history/search.html')


@login_required
@allowed_users(role='supervisor_ict')
def history_report(request):
    if request.method == 'POST':
        serial = request.POST['entry']
        date = datetime.today().strftime('%Y-%m-%d')
        # Get current owner details
        try:
            data = Comp.objects.get(asset_serial__icontains=serial)
            dat = Client.objects.filter(
                asset_assigned__icontains='NO', asset_serial__icontains=serial).order_by('-client_pk')
        except:
            data = ''
            dat = ''

        if data != '' and len(list(dat)) >= 0:
            context = {
                'data': data,
                'date': date,
                'dat': dat,
            }
            return render(request, 'asset/owner_history/report.html', context)
        else:
            return render(request, 'asset/owner_history/norecord.html')
    else:
        return HttpResponse("Invalid URL")

# Asset Report


@login_required
@allowed_users(role='supervisor_ict')
def asset_search(request):
    return render(request, 'asset/report/search.html')


@login_required
@allowed_users(role='supervisor_ict')
def asset_report(request):
    if request.method == 'POST':
        date = datetime.today().strftime('%Y-%m-%d')
        region = int(request.POST['region'])
        # region = Region.objects.get(region_pk=region)
        station = int(request.POST['station'])
        # station = Station.objects.get(station_pk=station)
        assettype = int(request.POST['asset_type'])
        # assettype = Assettype.objects.get(assettype_pk=station)

        # Get data
        try:
            data = Comp.objects.filter(
                region=region, station=station, assettype=assettype, condition__icontains='Working')

            count = data.count()
        except:
            data = ''

            count = ''

        if len(list(data)) > 0:
            context = {
                'data': data,
                'date': date,
                'count': count,
                'region': region,
                'station': station,
                'assettype': assettype,
            }
            return render(request, 'asset/report/report.html', context)
        else:
            return render(request, 'asset/report/norecord.html')
    else:
        return HttpResponse("Invalid URL")


@login_required
@allowed_users(role='supervisor_ict')
def excel_export(request):
    if request.method == 'POST':
        date = datetime.today().strftime('%Y-%m-%d')
        region = request.POST['region']
        station = request.POST['station']
        assettype = request.POST['assettype']
        response = HttpResponse(content_type='text/csv')
        response['content-Disposition'] = 'attachment; filename="Asset_Report.csv" '
        writer = csv.writer(response)
        writer.writerow(['Asset Type', 'Asset Serial', 'Asset Model', 'Monitor Model', 'Monitor Serial', 'OS', 'Domain', 'ADSS', 'LAPS', 'KAV', 'WOL',
                        'IP ADDRESS', 'EXTENSION', 'CONDITION', 'Staff Name', 'Staff Number', 'Department', 'Section', 'Region', 'Station', 'Date Assigned'])
        data = Comp.objects.filter(region=region, station=station, assettype=assettype).values_list('assettype__name', 'asset_serial', 'asset_model', 'monitor__monitor_model', 'monitor__monitor_serial', 'os', 'domain', 'adss',
                                                                                                    'laps', 'kaspersky', 'wol', 'ip_address', 'extension', 'condition', 'client__full_name', 'client__staff_number', 'client__department', 'client__section', 'region__name', 'station__name', 'client__date_assigned')
        for d in data:
            writer.writerow(d)
        return response
    else:
        return HttpResponse("Invalid URL")


# Unassigned assets
@login_required
@allowed_users(role='supervisor_ict')
def free_search(request):
    return render(request, 'asset/free_assets/search.html')


@login_required
@allowed_users(role='supervisor_ict')
def free_report(request):
    if request.method == 'POST':
        date = datetime.today().strftime('%Y-%m-%d')
        region = request.POST['region']
        station = request.POST['station']
        assettype = request.POST['assettype']
        # Get data from database

        try:
            data = Comp.objects.filter(
                condition__icontains='Working', region=region, station=station, client__staff_number='ICT')
            count = data.count()
        except:
            data = ''
            count = ''

        if len(list(data)) > 0 and count != 0:
            context = {
                'data': data,
                'count': count,
                'date': date,
            }
            return render(request, 'asset/free_assets/report.html', context)
        else:
            return render(request, 'asset/free_assets/norecord.html')
    else:
        return HttpResponse("Invalid URL")


# Obsolete Assets
@login_required
@allowed_users(role='supervisor_ict')
def obso_search(request):
    return render(request, 'asset/obso_assets/search.html')


@login_required
@allowed_users(role='supervisor_ict')
def obso_report(request):
    if request.method == 'POST':
        date = datetime.today().strftime('%Y-%m-%d')
        region = request.POST['region']
        station = request.POST['station']
        assettype = request.POST['assettype']
        # Get data from database

        try:
            data = Comp.objects.filter(condition__icontains='OBSOLETE', region=region,
                                       station=station, assettype=assettype, client__staff_number='ICT')
            count = data.count()
        except:
            data = ''
            count = ''

        if len(list(data)) > 0 and count != 0:
            context = {
                'data': data,
                'count': count,
                'date': date,
            }
            return render(request, 'asset/obso_assets/report.html', context)
        else:
            return render(request, 'asset/obso_assets/norecord.html')
    else:
        return HttpResponse("Invalid URL")
