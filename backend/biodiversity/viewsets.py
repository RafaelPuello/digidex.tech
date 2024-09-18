from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Plant, PlantImage, PlantDocument
from .serializers import PlantSerializer, PlantImageSerializer, PlantDocumentSerializer


class PlantViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing plants.
    """

    queryset = Plant.objects.all().order_by('id')
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['id', 'name', 'description', 'images', 'documents']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show plant images associated with each user.
        """
        return Plant.objects.filter(user=self.request.user)


class PlantImageSerializerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing NFC tags.
    """

    queryset = PlantImage.objects.all()
    serializer_class = PlantImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['id', 'image', 'caption', 'sort_order']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show plant images associated with each user.
        """
        return PlantImage.objects.filter(user=self.request.user)


class PlantDocumentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing plant documents.
    """

    queryset = PlantDocument.objects.all()
    serializer_class = PlantDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['id', 'document', 'caption', 'sort_order']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show plant documents associated with the user.
        """
        return PlantDocument.objects.filter(user=self.request.user)
