from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from . import get_nfc_tag_model
from .models import NFCTagScan
from .serializers import NFCTagSerializer, NFCTagScanSerializer


class NFCTagViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing NFC Tags.
    """
    queryset = get_nfc_tag_model().objects.all()
    serializer_class = NFCTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'serial_number'
    body_fields = ['serial_number', 'design']
    meta_fields = ['id']

    def get_queryset(self):
        return get_nfc_tag_model().objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new NFC tag with the provided serial number and tag type.
        """
        serial_number = request.data.get('serial_number')

        if not serial_number:
            return Response({"error": "Serial Number not provided."}, status=status.HTTP_400_BAD_REQUEST)

        ntag, created = get_nfc_tag_model().objects.update_or_create(
            serial_number=serial_number
        )

        serializer = self.get_serializer(ntag, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Set active to False for now. Will fix later.
        """
        instance = self.get_object()
        instance.active = False
        # self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NFCTagScanViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing an NFC Tag's Scans.
    """
    queryset = NFCTagScan.objects.all()
    serializer_class = NFCTagScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['ntag', 'scan_time']
    meta_fields = ['id']

    def get_queryset(self):
        return NFCTagScan.objects.filter(ntag__user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new NFC tag scan with the provided NFC tag ID and scan time.
        """

        ntag_id = request.data.get('ntag_id')
        scan_time = request.data.get('scan_time')

        if not ntag_id:
            return Response({"error": "NFC Tag ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ntag = get_nfc_tag_model().objects.get(pk=ntag_id)
        except get_nfc_tag_model().DoesNotExist:
            return Response({"error": "Invalid NFC Tag ID."}, status=status.HTTP_400_BAD_REQUEST)

        ntag_scan = NFCTagScan.objects.create(
            ntag=ntag,
            scan_time=scan_time
        )

        serializer = self.get_serializer(ntag_scan, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
