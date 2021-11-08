from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from comp.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from django.contrib import messages
import random
import string
from asset.models import *
from asset.communications import *
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

#Display staff home page, Display Staff Assigned Assets
@login_required
def user_home(request):
    loggedin = request.user
    client_number = loggedin.username
    date = datetime.today().strftime('%Y-%m-%d')
   
    try:
        data = Comp.objects.filter(client__staff_number__icontains= client_number, client__asset_assigned = 'Yes')[:1]
            
            
        dat = Comp.objects.filter(client__staff_number__icontains = client_number, client__asset_assigned = 'Yes', ict_approval='Approved')
        num = dat.count()
    except:
        data = []
            
        dat = []
        num = ''
    
    if len(list(data))>0 and len(list(dat))>0 and num != '':       
        context = {
                'data': data,
                'dat': dat,
                'date':date,
                'num':num,
                'loggedin':loggedin,
        }
        return render(request,'staff/my_assets/user_assets.html',context)
    else:
        context = {
                'date':date,
                'loggedin':loggedin,
        }
        return render(request,'staff/my_assets/noasset.html',context)

#Display my asset repairs page
@login_required
def my_asset_repairs(request):
    #Getting repairs data from the database
    usernumber = request.user.username
    try:
        data = Repair.objects.filter(comp__client__staff_number=usernumber).order_by('-cdate', '-rdate')
    except:
        data = []
    
    if len(list(data)) > 0:
        #pagination
        page = request.GET.get('page', 1)

        paginator = Paginator(data, 10)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    
        context = {
            'page_obj':page_obj
            }
        return render(request, 'staff/my_assets_repairs/repairs.html', context)
    else:
        return render(request, 'staff/my_assets_repairs/norepairs.html')

#send a  service request
@login_required
def service_request(request):
    if request.method == 'GET':
        return render(request, 'staff/service_request/service.html')
                
    if request.method == 'POST':
        letters = string.ascii_uppercase
        number = ''.join(random.choice(letters) for i in range(20))
        date = datetime.today().strftime('%Y-%m-%d')
        staff_number = request.user.username
        asset_serial = request.POST['asset_serial'].strip()
        service = request.POST['service'].strip()
        reason = request.POST['reason'].strip()
        
        #Check if asset exists in the database
        if Comp.objects.filter(asset_serial__icontains=asset_serial).count() > 0:
            #check if staff is assigned that asset
            if Client.objects.filter(comp__asset_serial__icontains=asset_serial,staff_number__icontains=staff_number).count() > 0:
                
                #Get staff details
                c = Client.objects.get(comp__asset_serial__icontains=asset_serial,staff_number__icontains=staff_number)
                
                name = c.full_name
                address = c.staff_email
                
                # send mail
                subject = service + ' ' + ' - ' + name  + ' ' + ' - '+ number
                body = f"Dear {name}, your service request has been received, and it is being acted upon. \n \n Regards \n IASSET Team"
                
                try:
                    send_mail(subject, 
                    body, EMAIL_HOST_USER, [address,'ictmsa43@gmail.com'], fail_silently = False)
                    
                    #Insert the record in the database
                    comp_id = Comp.objects.get(asset_serial__icontains=asset_serial)
                    r = Requested(request_number=number,request_service=service,request_reason=reason,request_date=date,comp=comp_id)
                    r.save()
                    
                    # Flash message and redirect to home page
                    messages.success(request, f"Service Request send successfully!!")
                    return redirect('staff_home')    
                    
                except:
                    # Flash message and redirect to home page
                    messages.success(request, f"Check your internet connection and try again!!")
                    return redirect('staff_home')    
                
            else:
                # Flash message and redirect to home page
                messages.success(request, f"You are not assigned that asset!!")
                return redirect('staff_home')
                
        else:
            # Flash message and redirect to home page
            messages.success(request, f"No such Asset serial Number in the database!!")
            return redirect('staff_home')
        
#My Asset Approvals
@login_required
def my_asset_approvals(request):
    client_number = request.user.username
   
    try:     
        dat = Comp.objects.exclude(ict_approval='Approved').filter(client__staff_number__icontains = client_number, client__asset_assigned = 'Yes')
    except:    
        dat = ""
        
    if len(list(dat)) > 0:
        context = {
                'dat': dat,
            }
        return render(request, 'staff/my_approvals/approvals.html', context)
    else:
        return render(request, 'staff/my_approvals/noapprovals.html')

#Hod Approvals
@login_required
def hod_approvals(request):
    client_number = request.user.username
    
    try:     
        dat = Comp.objects.filter(client__hod__hod_number__icontains = client_number, client__asset_assigned = 'Yes', client__hod_approval='Pending')
    except:
        dat = []
    
    if len(list(dat)) > 0:
        page = request.GET.get('page', 1)

        paginator = Paginator(dat, 10)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    
            
        context = {
            'page_obj': page_obj,
            }
        
        return render(request, 'staff/hod_approvals/hod_approvals.html', context)
    else:
        return render(request, 'staff/hod_approvals/noapprovals.html')

# staff asset accept
@login_required
def staff_accept(request):
    if request.method == 'GET':
        serial = request.GET['serial'].strip()
        
        if Client.objects.get(comp__asset_serial=serial).hod_approval == 'Approved':
                  
            if Client.objects.get(comp__asset_serial=serial).accepted == 'Pending':
                Client.objects.filter(comp__asset_serial=serial).update(accepted='Accepted')
            
                # email_ict(serial)
                # Flash message and redirect to home page
                messages.success(request, f"Successfully accepted Ict Asset Assigned to you!!!")
                return redirect('my_asset_approvals')
            else:
                # email_ict(serial)
                # Flash message and redirect to home page
                messages.info(request, f"You have already accepted or rejected Ict Asset Assigned to you!!!")
                return redirect('my_asset_approvals')
        else:
            # Flash message and redirect to home page
            messages.info(request, f"Your HOD has not Approved Ict Asset Assigned to you!!!")
            return redirect('my_asset_approvals')
        
# HOD asset approval
@login_required
def hod_asset_approval(request):
    if request.method == 'GET':
        serial = request.GET['serial'].strip()
        
        if Client.objects.get(comp__asset_serial=serial).hod_approval == 'Pending':
                Client.objects.filter(comp__asset_serial=serial).update(hod_approval='Approved')
            
                # email_ict(serial)
                # Flash message and redirect to home page
                messages.success(request, f"Successfully approved Ict Asset Assigned to your staff!!!")
                return redirect('hod_approvals')
        else:
            # Flash message and redirect to home page
            messages.info(request, f"You have already Approved Ict Asset Assigned to your staff!!!")
            return redirect('hod_approvals')
                  
                  
          
