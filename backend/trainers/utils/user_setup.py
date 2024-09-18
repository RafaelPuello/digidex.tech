from django.contrib.auth.models import Group

from .collection_setup import setup_user_collection
from .group_setup import get_trainer_group


def setup_new_trainer(user):
    user_group, _ = Group.objects.get_or_create(name=user.uuid)
    user.groups.add(user_group)
    setup_user_collection(user, user_group)

    user.create_trainer_page()
    trainer_group = get_trainer_group()
    user.groups.add(trainer_group)
    return
