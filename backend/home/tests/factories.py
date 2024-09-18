import factory
from wagtail.models import Page, Locale, Site

from home.models import HomePage


class LocaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Locale
        django_get_or_create = ('language_code',)

    language_code = 'en'


class HomePageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HomePage

    title = "Home"
    slug = "home"
    locale = factory.SubFactory(LocaleFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to ensure that the HomePage
        is added to the Wagtail page tree correctly.
        """
        home = model_class(**kwargs)
        
        root = Page.get_first_root_node()
        if root:
            home = root.add_child(instance=home)
        else:
            home = Page.add_root(instance=home)
        home.save_revision().publish()

        Site.objects.create(
            hostname='testsite',
            port=80,
            root_page=home,
            is_default_site=True,
            site_name='Test Site'
        )
        return home
