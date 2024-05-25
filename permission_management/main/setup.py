from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def create_groups_and_permissions():
    # Groups
    admins, _ = Group.objects.get_or_create(name='Admins')
    editors, _ = Group.objects.get_or_create(name='Editors')
    viewers, _ = Group.objects.get_or_create(name='Viewers')

    # Permissions
    content_type = ContentType.objects.get_for_model(User)
    
    dashboard_access = Permission.objects.create(codename='dashboard_access', name='Can access dashboard', content_type=content_type)
    reports_view = Permission.objects.create(codename='reports_view', name='Can view reports', content_type=content_type)
    reports_edit = Permission.objects.create(codename='reports_edit', name='Can edit reports', content_type=content_type)
    settings_access = Permission.objects.create(codename='settings_access', name='Can access settings', content_type=content_type)
    
    # Assign permissions to groups
    admins.permissions.add(dashboard_access, reports_view, reports_edit, settings_access)
    editors.permissions.add(reports_view, reports_edit)
    viewers.permissions.add(reports_view)
