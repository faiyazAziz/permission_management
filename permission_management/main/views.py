from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ReportForm
from .models import ReportData,AuditLog
from django.http import HttpResponse



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
        else:
            print(form.errors)  # Print form errors to console
            messages.error(request, 'Invalid form submission. Please correct the errors.')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    response = HttpResponse()
    if 'sessionid' in request.COOKIES:
        response.delete_cookie('sessionid')
    return redirect('login')

@login_required
def home(request):
    return render(request, 'main/home.html')

@login_required
@permission_required('auth.dashboard_access', raise_exception=True)
def dashboard(request):
    return render(request, 'main/dashboard.html')

@login_required
@permission_required('auth.reports_view', raise_exception=True)
def reports(request):
    has_reports_edit_perm = request.user.has_perm('auth.reports_edit')

    if request.method == 'POST' and has_reports_edit_perm:
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            return redirect('reports')
    else:
        form = ReportForm()

    reports = ReportData.objects.all()
    return render(request, 'main/reports.html', {'form': form, 'reports': reports, 'has_reports_edit_perm': has_reports_edit_perm})

@login_required
@permission_required('auth.settings_access', raise_exception=True)
def settings(request):
    return render(request, 'main/settings.html')


from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import UserForm, GroupForm,GroupPermissionsForm,UserPermissionsForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

def is_admin(user):
    return user.groups.filter(name='Admins').exists()

@method_decorator(user_passes_test(is_admin), name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'main/user_list.html'
    context_object_name = 'users'
    
@method_decorator(user_passes_test(is_admin), name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'main/user_form.html'
    success_url = reverse_lazy('user_list')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'main/user_form.html'
    success_url = reverse_lazy('user_list')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'main/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class GroupListView(ListView):
    model = Group
    template_name = 'main/group_list.html'
    context_object_name = 'groups'

@method_decorator(user_passes_test(is_admin), name='dispatch')
class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'main/group_form.html'
    success_url = reverse_lazy('group_list')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'main/group_form.html'
    success_url = reverse_lazy('group_list')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'main/group_confirm_delete.html'
    success_url = reverse_lazy('group_list')

@method_decorator(user_passes_test(is_admin), name='dispatch')
class UserPermissionsUpdateView(UpdateView):
    model = User
    form_class = UserPermissionsForm
    template_name = 'main/user_permissions_form.html'
    success_url = reverse_lazy('user_list')
    
@method_decorator(user_passes_test(is_admin), name='dispatch')
class GroupPermissionsUpdateView(UpdateView):
    model = Group
    form_class = GroupPermissionsForm
    template_name = 'main/group_permissions_form.html'
    success_url = reverse_lazy('group_list')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class AuditLogListView(ListView):
    model = AuditLog
    template_name = 'main/audit_log_list.html'
    context_object_name = 'audit_logs'
    ordering = ['-action_time']