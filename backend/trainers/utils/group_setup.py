from django.contrib.auth.models import Permission, Group

def get_trainer_group():
    group, created = Group.objects.get_or_create(name='Trainers')
    if created:
        group = create_trainer_group_permissions(group)
    return group

def create_trainer_group_permissions(group):
    PERMISSIONS = [
        "add_plant", "change_plant", "delete_plant",
        "add_box", "change_box", "delete_box",
        "access_admin",
        ]
    
    permissions = Permission.objects.filter(
        codename__in=PERMISSIONS
    )
    group.permissions.add(*permissions)
    group.save()
    return group
