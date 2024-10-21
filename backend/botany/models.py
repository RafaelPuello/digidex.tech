import uuid
from django.db import models, transaction
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from wagtail.models import Orderable

from base.models import BaseImage
from ntags.models import BaseNFCTag

from .forms import UserPlantAdminForm


class PlantSubstrate(models.Model):
    """
    This model represents different substrates for growing plants.
    Examples include soil, hydroponics, coco coir, etc.
    """
    name = models.CharField(
        max_length=255,
        unique=True
    )
    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = _('Plant Substrate')
        verbose_name_plural = _('Plant Substrates')

    def __str__(self):
        return self.name


class SubstrateMix(models.Model):
    """
    This model represents a mixture of substrates for growing plants.
    Examples include 50% soil, 50% perlite, etc.
    """
    name = models.CharField(
        max_length=255,
        unique=True
    )
    description = models.TextField(
        blank=True
    )
    substrates = models.ManyToManyField(
        PlantSubstrate,
        related_name='mixes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='substrate_mixes',
        on_delete=models.SET_NULL
    )
    metadata = models.JSONField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Substrate Mix')
        verbose_name_plural = _('Substrate Mixes')

    def __str__(self):
        return self.name


class PlantNote(models.Model):
    plant = ParentalKey(
        'UserPlant',
        related_name='notes',
        on_delete=models.CASCADE
    )
    heading = models.CharField(
        max_length=255,
        blank=True
    )
    content = RichTextField()
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.plant.name}'s note"

    class Meta:
        verbose_name = _('Plant Note')
        verbose_name_plural = _('Plant Notes')


class UserPlant(Orderable, ClusterableModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    slug = models.SlugField(
        editable=False,
        db_index=True,
        max_length=255
    )
    box = models.ForeignKey(
        'inventory.InventoryBox',
        related_name='plants',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=255,
        db_index=True
    )
    description = models.TextField(
        blank=True
    )
    image = models.ForeignKey(
        BaseImage,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True,
        null=True
    )
    taxon_id = models.PositiveBigIntegerField(
        blank=True,
        default=6
    )
    substrate = models.ForeignKey(
        SubstrateMix,
        related_name='+',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    active = models.BooleanField(
        default=False
    )

    base_form_class = UserPlantAdminForm

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('plant')
        verbose_name_plural = _('plants')
        indexes = [
            models.Index(fields=['box', 'name']),
            models.Index(fields=['box', 'slug']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['box', 'name'], name='unique_plant_name_in_box'),
            models.UniqueConstraint(fields=['box', 'slug'], name='unique_plant_slug_in_box'),
        ]

    @property
    def url(self):
        return self.get_url()

    def get_url(self):
        return self.box.url + slugify(self.name) + '/'

    @property
    def collection(self):
        return self.get_parent_collection()

    def get_parent_collection(self):
        return self.user.collection

    def get_inventory_form(self, request):
        tasks = {}

        form = self.box.get_form(page=self.box, user=request.user)
        if form:
            tasks.update({
                'form': form,
                # 'form_fields': self.box.get_inventory_form_fields(),
                'form_url': self.box.get_url(request)
            })

        return tasks

    @transaction.atomic
    def create_copies(self, copies):
        """
        Creates specified number of copies of this UserPlant instance.
        """
        if copies < 1:
            raise ValueError("Number of copies must be at least 1.")

        plant_copies = []

        for copy_number in range(1, copies + 1):
            plant_copy = UserPlant.objects.create(
                box=self.box,
                name=f"{self.name} - {copy_number}",
                description=self.description,
            )
            plant_copies.append(plant_copy)

        # Bulk create all plant copies for efficiency
        # UserPlant.objects.bulk_create(plant_copies, ignore_conflicts=True)
        return plant_copies
