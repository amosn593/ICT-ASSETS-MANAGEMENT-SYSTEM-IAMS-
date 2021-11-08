from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_home, name='staff_home'),
    path('service_request/', views.service_request, name='service_request'),
    path('my_asset_repairs/', views.my_asset_repairs, name='my_asset_repairs'),
    path('my_asset_approvals/', views.my_asset_approvals, name='my_asset_approvals'),
    path('hod_approvals/', views.hod_approvals, name='hod_approvals'),
    path('staff_accept/', views.staff_accept, name='staff_accept'),
    path('hod_asset_approval/', views.hod_asset_approval, name='hod_asset_approval'),
    
    ]
