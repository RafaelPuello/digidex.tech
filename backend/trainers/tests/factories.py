import factory
import uuid
from django.contrib.auth.models import Group
from wagtail.models import Collection

from home.models import HomePage
from home.tests.factories import HomePageFactory
from trainers.models import Trainer, TrainerPage


class TrainerCollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    name = factory.LazyAttribute(lambda obj: f"Trainer Collection {obj.trainer_uuid}")
    parent = factory.SubFactory(HomePageFactory)
    trainer_uuid = factory.SelfAttribute('trainer.uuid')


class TrainerGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group


class TrainerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trainer

    # Generate a UUID before creating the Trainer instance
    uuid = factory.LazyFunction(uuid.uuid4)
    first_name = 'Test'
    last_name = 'Trainer'
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    username = factory.LazyAttribute(lambda obj: f"trainer_{obj.uuid}")
    password = factory.PostGenerationMethodCall('set_password', 'password123')

    # Pass the trainer's UUID to the collection and group factories
    collection = factory.SubFactory(
        TrainerCollectionFactory,
        trainer_uuid=factory.SelfAttribute('uuid')
    )
    group = factory.SubFactory(
        TrainerGroupFactory,
        trainer_uuid=factory.SelfAttribute('uuid')
    )


class TrainerPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TrainerPage

    # Owner is created using the updated TrainerFactory
    owner = factory.SubFactory(TrainerFactory)

    # Use the owner's username for title and slug
    title = factory.LazyAttribute(lambda obj: obj.owner.username)
    slug = factory.LazyAttribute(lambda obj: obj.owner.username)

    @factory.post_generation
    def add_to_tree(self, create, extracted, **kwargs):
        if create:
            home_page = HomePage.objects.first()
            home_page.add_child(instance=self)
            self.save_revision().publish()
