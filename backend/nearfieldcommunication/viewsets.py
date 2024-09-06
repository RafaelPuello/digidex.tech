from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import NfcTag, NfcTagType
from .serializers import NfcTagSerializer, NfcTagTypeSerializer


class NfcTagTypeViewSet(viewsets.ModelViewSet):
    queryset = NfcTagType.objects.all().order_by('id')
    serializer_class = NfcTagTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['name', 'description']
    meta_fields = ['id']

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        description = request.data.get('description')

        if not name:
            return Response({"error": "Name not provided."}, status=status.HTTP_400_BAD_REQUEST)

        nfc_tag_type, created = NfcTagType.objects.update_or_create(
            name=name,
            defaults={'description': description}
        )

        serializer = self.get_serializer(nfc_tag_type, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class NfcTagViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing NFC tags.
    """

    serializer_class = NfcTagSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'serial_number'
    body_fields = ['serial_number', 'nfc_tag_type']
    meta_fields = ['id']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return NfcTag.objects.all()
        return NfcTag.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number')
        tag_type_id = request.data.get('tag_type_id')

        if not serial_number:
            return Response({"error": "Serial Number not provided."}, status=status.HTTP_400_BAD_REQUEST)

        if tag_type_id:
            try:
                nfc_tag_type = NfcTagType.objects.get(pk=tag_type_id)
            except NfcTagType.DoesNotExist:
                return Response({"error": "Invalid Tag Type ID."}, status=status.HTTP_400_BAD_REQUEST)

        nfc_tag, created = NfcTag.objects.update_or_create(
            serial_number=serial_number,
            defaults={'nfc_tag_type': nfc_tag_type}
        )

        serializer = self.get_serializer(nfc_tag, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Just set active to False for now. Will set permissions later.
        """
        instance = self.get_object()
        instance.active = False
        # self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
