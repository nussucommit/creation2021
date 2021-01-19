from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            if request.user.is_superuser:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not allowed to view this page')
            return view_func(request,*args,**kwargs)
        return wrapper_func
    return decorator