from wagtail import hooks

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['biodiversity/icons/plant.svg']
