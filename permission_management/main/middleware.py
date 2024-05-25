from django.shortcuts import redirect
from django.urls import reverse
import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)


class CheckPermissionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if not request.user.is_authenticated:
        #     return redirect(reverse('login'))

        # if not request.user.has_perm('app_label.permission_name'):
        #     return redirect(reverse('permission_denied'))
        _thread_locals.user = request.user
        response = self.get_response(request)
        return response
