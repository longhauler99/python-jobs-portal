from django.shortcuts import redirect
from functools import wraps

def unauthenticated_user(redirect_url='jobs'):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator