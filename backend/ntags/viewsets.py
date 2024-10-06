from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from rest_framework.decorators import action
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect

from .models import NFCTag
from .serializers import NFCTagSerializer


class NFCTagViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, and linking NFC tags.
    """
    queryset = NFCTag.objects.all()
    serializer_class = NFCTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'serial_number'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return NFCTag.objects.all()
        return NFCTag.objects.filter(
            user=self.request.user,
            active=True
        )

    def create(self, request, *args, **kwargs):
        """
        Create a new NFC tag with the provided serial number.
        """
        serial_number = request.data.get('serial_number')

        if not serial_number:
            return Response({"error": "Serial Number not provided."}, status=status.HTTP_400_BAD_REQUEST)

        ntag, created = NFCTag.objects.update_or_create(
            serial_number=serial_number
        )

        serializer = self.get_serializer(ntag, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Perform actual deletion if the user is a superuser, otherwise set
        the NFC tag's active status to False.
        """
        instance = self.get_object()

        if request.user.is_superuser:
            # Perform the usual delete if the user is a superuser
            return super().destroy(request, *args, **kwargs)
        else:
            # For regular users, set 'active' to False instead of deleting
            instance.active = False
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='link')
    def link(self, request):
        """
        Custom action to link an NTAG using the ASCII Mirror embedded in the NTAG's URL.
        """
        mirrored_values = request.GET.get('m', None)

        if not mirrored_values:
            return Response({"error": "Invalid mirror values."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ntag = NFCTag.objects.get_from_mirror(mirrored_values)
            return redirect(ntag.url)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path=r'linkable-objects/(?P<objects_id>\d+)')
    def get_linkable_objects(self, request, objects_id=None):
        """
        Custom action to get the objects that can be linked to an NTAG.
        """
        try:
            content_type = ContentType.objects.get(id=objects_id)
            model_class = content_type.model_class()
            objects = model_class.objects.all()

            data = {
                'objects': [{'id': obj.id, 'name': str(obj)} for obj in objects]
            }

            return Response(data)

        except ContentType.DoesNotExist:
            return Response({'error': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)
