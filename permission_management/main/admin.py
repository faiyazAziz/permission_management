# from django.contrib import admin
# from django.contrib.auth.models import Group
# from django.contrib.auth.admin import GroupAdmin
# from .models import ReportData,AuditLog

# admin.site.unregister(Group)
# admin.site.register(ReportData)
# admin.site.register(AuditLog)

# @admin.register(Group)
# class CustomGroupAdmin(GroupAdmin):
#     pass


# from django.contrib.admin import AdminSite
# from django.contrib.auth.models import Group
# from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

# class GroupAdmin(BaseGroupAdmin):
#     # Customize the GroupAdmin as needed
#     pass

# class MyAdminSite(AdminSite):
#     site_header = 'Custom Admin Panel'
#     site_title = 'Custom Admin Panel'
#     index_title = 'Welcome to the Custom Admin Panel'

# my_admin_site = MyAdminSite(name='myadmin')
# my_admin_site.register(Group, GroupAdmin)

# from django.contrib import admin
# from django.contrib.auth.models import Group

# class GroupAdmin(admin.ModelAdmin):
#     filter_horizontal = ['permissions']

# admin.site.unregister(Group)
# admin.site.register(Group, GroupAdmin)


# admin.py

from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import AuditLog

# class CustomUserAdmin(admin.ModelAdmin):
#     actions = ['add_to_group']

#     def add_to_group(self, request, queryset):
#         selected_users = queryset.values_list('id', flat=True)
#         selected_group_id = request.POST.get('group_id')  # Assuming group_id is passed as a POST parameter
#         group = Group.objects.get(id=selected_group_id)
#         users_added = []
#         for user_id in selected_users:
#             user = User.objects.get(id=user_id)
#             user.groups.add(group)
#             users_added.append(user.username)
#             # Log the action in the audit log
#             AuditLog.objects.create(
#                 action='ADD_TO_GROUP',
#                 user=request.user,
#                 description=f'Added user {user.username} to group {group.name}'
#             )
#         self.message_user(request, f'Users {", ".join(users_added)} added to group {group.name}.')
#     add_to_group.short_description = 'Add selected users to group'


from .models import AuditLog,ReportData
admin.site.register(AuditLog)
admin.site.register(ReportData)