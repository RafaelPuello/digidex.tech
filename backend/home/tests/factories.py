import factory
from wagtail.models import Page, Locale, Site

from home.models import HomePage


class LocaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Locale
        django_get_or_create = ('language_code',)

    language_code = 'en'


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site

    hostname = "testserver"
    root_page = Page.get_first_root_node()
    is_default_site = True
    site_name = "Test Site"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to ensure pages
        are added to the Wagtail page tree correctly.
        """
        root = Page.get_first_root_node()
        return Site.objects.create(
            hostname=kwargs['hostname'],
            root_page=root,
            is_default_site=kwargs['is_default_site'],
            site_name=kwargs['site_name'],
        )


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
        
        site = factory.SubFactory(SiteFactory())
        site.root.add_child(instance=home)

        home.save_revision().publish()
        return home
