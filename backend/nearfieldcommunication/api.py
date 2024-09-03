from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from wagtail.api.v2.views import BaseAPIViewSet

from .models import NfcTag, NfcTagType
from .serializers import NfcTagSerializer


class NfcTagAPIViewSet(BaseAPIViewSet):
    model = NfcTag
    base_serializer_class = NfcTagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'serial_number'
    body_fields = ['serial_number', 'nfc_tag_type']
    meta_fields = ['id']

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
