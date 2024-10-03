from django.contrib.auth.models import Group


def get_trainer_group():
    group, created = Group.objects.get_or_create(name="Trainers")
    return group
