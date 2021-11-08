from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauthenticate_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(role = ''):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = []
            if request.user.groups.exists():
                x = 0
                while x < len(request.user.groups.all()):
                    group.append(request.user.groups.all()[x].name)
                    x += 1
            if role in group:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'staff/auth/ict.html')
        return wrapper_func
    return decorator

def allowed_admin(role = ''):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = []
            if request.user.groups.exists():
                x = 0
                while x < len(request.user.groups.all()):
                    group.append(request.user.groups.all()[x].name)
                    x += 1
            if role in group:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'asset/auth/admin.html')
        return wrapper_func
    return decorator