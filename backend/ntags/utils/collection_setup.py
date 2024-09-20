from wagtail.models import Collection

def get_root_collection():
    root_col = Collection.get_first_root_node()
    if not root_col:
        raise Exception("Root collection not found. Please ensure a root collection exists.")
    return root_col

def get_collection(parent=None, name="ntags"):
    if parent is None:
        parent = Collection.get_first_root_node()
    try:
        return parent.get_children().get(name=name)
    except Collection.DoesNotExist:
        return parent.add_child(instance=Collection(name=name))
