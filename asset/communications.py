from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from comp.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from .models import *

#Sending deployment report
def email_client(id):
    #Sending acceptance mail to the staff
    data = Comp.objects.get(asset_serial=id)
    context = {
        'data':data,
    }
    subject = 'ICT ASSET DEPLOYMENT FORM' 
    html_message = render_to_string('asset/mail/client.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = data.client.staff_email 
    
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    
    
#Sending deployment report to HOD
def email_hod(id):
    #Sending approval mail to Hod
    data = Comp.objects.get(asset_serial=id)
    context = {
        'data':data,
    }
    subject = 'ICT ASSET DEPLOYMENT FORM FOR YOUR STAFF' 
    html_message = render_to_string('asset/mail/hod.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = data.client.hod.hod_email 
    
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
 
#Notifying ICT officer of HOD of affected user's Approval
def email_deliver(id):
    #Sending approval mail to ICT admin
    admin_email = User.objects.get(comp__asset_serial=id).email
    
    data = Comp.objects.get(asset_serial=id)
    context = {
        'data':data,
    }
    
    subject = 'ICT ASSET DEPLOYMENT - DELIVERY' 
    html_message = render_to_string('asset/mail/deliver.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = admin_email 
    
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)



   
#Sending deployment form to ICT admin for approval
def email_ict(id):
    #Sending approval mail to ICT admin
    admin_email = User.objects.get(comp__asset_serial=id).email
    context = {
        'id':id,
    }
    subject = 'ICT ASSET DEPLOYMENT FORM - ICT APPROVAL' 
    html_message = render_to_string('asset/mail/ict.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = admin_email 
    
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
  
    
#Sending Final deployment report 
def email_approve(id):
    #Sending deployment report 
    data = Comp.objects.get(asset_serial=id)
    context = {
        'data':data,
    }
    subject = 'ICT ASSET DEPLOYMENT REPORT' 
    html_message = render_to_string('asset/mail/final.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = data.client.staff_email
    to1 = data.client.hod.hod_email
    
    send_mail(subject, plain_message, from_email, [to, to1], html_message=html_message)
    
    
"""
Asset Movement emails
"""

#Relocate asset mail
def asset_relocate(id):
    data = Comp.objects.get(asset_serial=id)
    
    context = {
        'data':data,
    }
    subject = 'ICT ASSET RELOCATION REPORT ' 
    html_message = render_to_string('asset/relocate/relocate_mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = data.client.staff_email
    to1 = data.client.hod.hod_email
    
    send_mail(subject, plain_message, from_email, [to, to1], html_message=html_message)
    
#Replace monitor mail
def replace_monitor(id):
    data = Comp.objects.get(asset_serial=id)
    
    context = {
        'data':data,
    }
    subject = 'ICT ASSET MONITOR REPLACEMENT REPORT' 
    html_message = render_to_string('asset/monitor/monitor_mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = data.client.staff_email
    to1 = data.client.hod.hod_email
    
    send_mail(subject, plain_message, from_email, [to, to1], html_message=html_message)
    

#Surrender asset mail
def surrender_asset(id, client):
    data = Comp.objects.get(asset_serial=id)
    dat = Client.objects.get(client_pk=client)
    
    context = {
        'data':data,
        'dat':dat,
    }
    subject = 'ICT ASSET SURRENDER REPORT ' 
    html_message = render_to_string('asset/surrender/surrender_mail.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = dat.staff_email
    to1 = dat.hod.hod_email
    
    send_mail(subject, plain_message, from_email, [to, to1], html_message=html_message)
    
#Asset change ownership mail
def change_asset_ownership(id, client):
    data = Comp.objects.get(asset_serial=id)
    dat = Client.objects.get(client_pk=client)
    
    context = {
        'data':data,
        'dat':dat,
    }
    subject = 'ICT ASSET CHANGE OF OWNERSHIP REPORT ' 
    html_message = render_to_string('asset/ownership/change_email.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'ictmsa43@gmail.com' 
    to = dat.staff_email
    to1 = dat.hod.hod_email
    to2 = data.client.staff_email
    to3 = data.client.hod.hod_email
    
    send_mail(subject, plain_message, from_email, [to2, to3, to, to1], html_message=html_message)
    
    
        