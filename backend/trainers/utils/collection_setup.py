from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from wagtail.models import Collection, GroupCollectionPermission


def setup_user_collection(user, group):
    collection = create_user_collection(user)
    try:
        return create_collection_permissions(collection, group)
    except Exception as e:
        raise e


def create_user_collection(user):
    """
    Creates a collection for the given user if it does not already exist.
    The collection path will be: root -> trainer collection -> [user_uuid].

    Args:
        user (User): An instance of the User model.

    Returns:
        Collection: The created or retrieved collection instance.
    """
    # Check if the user already has a collection
    if user.collection:
        return user.collection

    # Get the root collection
    try:
        root_collection = Collection.get_first_root_node()
    except ObjectDoesNotExist:
        raise Exception("Root collection not found. Please ensure a root collection exists.")

    # Create the 'User Collection' under the root and save it
    root_user_collection = Collection(
        name="User Collections"
    )
    root_collection.add_child(instance=root_user_collection)
    root_user_collection.save()

    # Create the user's specific collection under the root 'User Collections'
    user_collection = Collection(
        name=user.uuid
    )
    root_user_collection.add_child(instance=user_collection)

    # Assign the collection to the user
    user.collection = user_collection
    user.save()
    return user_collection


def create_collection_permissions(collection, group):
    """
    Creates the necessary permissions for the given group on the given collection.
    The permissions include 'add_image', 'change_image', 'choose_image', 'add_document',
    'change_document', and 'choose_document'.

    Args:
        collection (Collection): An instance of the Collection model.
        group (Group): An instance of the Group model.

    Returns:
        Collection: The collection instance with permissions set.
    """
    PERMISSIONS = (
        'add_image', 'change_image', 'choose_image',
        'add_document', 'change_document', 'choose_document'
    )

    for perm in PERMISSIONS:
        permission = Permission.objects.get(codename=perm)
        GroupCollectionPermission.objects.create(
            group=group,
            collection=collection,
            permission=permission
        )
    return collection
