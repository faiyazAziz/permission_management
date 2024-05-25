from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission, User
from .models import AuditLog
from .middleware import get_current_user

# @receiver(post_save, sender=User)
# def add_to_admin_group(sender, instance, created, **kwargs):
#     if created:
#         admins_group = Group.objects.get(name='Admins')
#         instance.groups.add(admins_group)

@receiver(m2m_changed, sender=User.groups.through)
def log_user_group_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ["post_add", "post_remove"]:
        current_user = get_current_user()
        for pk in pk_set:
            group = Group.objects.get(pk=pk)
            if action == "post_add":
                action_desc = f"Group '{group.name}' added to user '{instance.username}'"
            else:
                action_desc = f"Group '{group.name}' removed from user '{instance.username}'"
            
            AuditLog.objects.create(
                action='Group Change',
                user=current_user,
                description=action_desc
            )
            
@receiver(m2m_changed, sender=Group.permissions.through)
def log_group_permission_change(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        group = instance
        current_user = get_current_user()
        permission_names = ', '.join([perm.codename for perm in group.permissions.all()])
        AuditLog.objects.create(
            action='Group Permission Change',
            user=current_user,
            description=f'Group {group.name} now has permissions: {permission_names}'
        )

@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            action='User Created',
            user=instance,
            description=f'User {instance.username} was created.'
        )


@receiver(m2m_changed, sender=User.user_permissions.through)
def log_permission_changes(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ["post_add", "post_remove"]:
        current_user = get_current_user()
        for pk in pk_set:
            permission = Permission.objects.get(pk=pk)
            if action == "post_add":
                action_desc = f"Permission '{permission.codename}' added to user '{instance.username}'"
            else:
                action_desc = f"Permission '{permission.codename}' removed from user '{instance.username}'"
            
            AuditLog.objects.create(
                action='Permission Change',
                user=current_user,
                description=action_desc
            )