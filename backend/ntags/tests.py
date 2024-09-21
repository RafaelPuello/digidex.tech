import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from wagtail.documents import get_document_model
from wagtail.images import get_image_model

from ntags.models import NFCTagDesign, Collection

User = get_user_model()


class NFCTagDesignModelTest(TestCase):

    def setUp(self):
        # Set up initial data for tests
        self.user = User.objects.create(username="testuser")
        self.root_collection = Collection.get_first_root_node()
        if not self.root_collection:
            self.root_collection = Collection.add_root(name="Root")
        self.ntag_design = NFCTagDesign.objects.create(
            name="Test Design",
            description="This is a test description.",
            designer=self.user,
        )

    def test_nfctagdesign_creation(self):
        """Test that an NFCTagDesign instance is correctly created."""
        self.assertEqual(self.ntag_design.name, "Test Design")
        self.assertEqual(self.ntag_design.description, "This is a test description.")
        self.assertEqual(self.ntag_design.designer, self.user)
        self.assertIsInstance(self.ntag_design.uuid, uuid.UUID)

    def test_nfctagdesign_unique_name(self):
        """Test that the name field must be unique."""
        with self.assertRaises(Exception):
            NFCTagDesign.objects.create(
                name="Test Design",  # Same name as self.ntag_design
                description="Another test description.",
                designer=self.user,
            )

    def test_get_documents(self):
        """Test the get_documents method."""
        document = get_document_model().objects.create(
            title="Test Document",
            collection=self.ntag_design.collection,
        )
        documents = self.ntag_design.get_documents()
        self.assertIn(document, documents)

    def test_get_images(self):
        """Test the get_images method."""
        image = get_image_model().objects.create(
            title="Test Image",
            collection=self.ntag_design.collection,
        )
        images = self.ntag_design.get_images()
        self.assertIn(image, images)

    def test_get_preview_template(self):
        """Test the get_preview_template method."""
        request = self.client.request()
        template = self.ntag_design.get_preview_template(request, "mode_name")
        self.assertEqual(template, "ntags/previews/design.html")

    def test_str_representation(self):
        """Test the string representation of the model."""
        self.assertEqual(str(self.ntag_design), "Test Design")

    def test_setup_collection_creates_new_collection(self):
        """Test that setup_collection creates a new collection if it doesn't exist."""
        new_ntag_design = NFCTagDesign.objects.create(
            name="New Test Design",
            designer=self.user,
        )
        self.assertIsNotNone(new_ntag_design.collection)
        self.assertTrue(Collection.objects.filter(name=new_ntag_design.uuid).exists())

    def test_setup_collection_uses_existing_collection(self):
        """Test that setup_collection uses an existing collection if it exists."""
        existing_collection = self.root_collection.add_child(name=self.ntag_design.uuid)
        self.ntag_design.collection = None
        self.ntag_design.save()

        self.assertEqual(self.ntag_design.collection, existing_collection)

    def test_save_method_creates_collection_if_not_exists(self):
        """Test that the save method creates a collection if none exists."""
        new_ntag_design = NFCTagDesign(
            name="Another Test Design",
            designer=self.user,
        )
        new_ntag_design.save()
        self.assertIsNotNone(new_ntag_design.collection)
        self.assertTrue(Collection.objects.filter(name=new_ntag_design.uuid).exists())
