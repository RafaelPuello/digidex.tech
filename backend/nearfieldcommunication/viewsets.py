from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import NfcTag, NfcTagType, NfcTagScan, NfcTagMemory
from .serializers import NfcTagSerializer, NfcTagTypeSerializer, NfcTagScanSerializer, NfcTagMemorySerializer


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
    queryset = NfcTag.objects.all()
    serializer_class = NfcTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'serial_number'
    body_fields = ['serial_number', 'nfc_tag_type']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show NFC tags needed for each role.
        """
        if self.request.user.is_superuser:
            return NfcTag.objects.all()
        elif self.request.user.groups.filter(name='Trainers').exists():
            return NfcTag.objects.filter(user=self.request.user)
        else:
            return NfcTag.objects.none()

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


class NfcTagScanViewSet(viewsets.ModelViewSet):
    queryset = NfcTagScan.objects.all()
    serializer_class = NfcTagScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['nfc_tag', 'scan_time']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show NFC tag scans needed for each role.
        """
        if self.request.user.is_superuser:
            return NfcTagScan.objects.all()
        elif self.request.user.groups.filter(name='Trainers').exists():
            return NfcTagScan.objects.filter(nfc_tag__user=self.request.user)
        else:
            return NfcTagScan.objects.none()

    def create(self, request, *args, **kwargs):
        nfc_tag_id = request.data.get('nfc_tag_id')
        scan_time = request.data.get('scan_time')

        if not nfc_tag_id:
            return Response({"error": "NFC Tag ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nfc_tag = NfcTag.objects.get(pk=nfc_tag_id)
        except NfcTag.DoesNotExist:
            return Response({"error": "Invalid NFC Tag ID."}, status=status.HTTP_400_BAD_REQUEST)

        nfc_tag_scan = NfcTagScan.objects.create(
            nfc_tag=nfc_tag,
            scan_time=scan_time
        )

        serializer = self.get_serializer(nfc_tag_scan, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NfcTagMemoryViewSet(viewsets.ModelViewSet):
    queryset = NfcTagMemory.objects.all()
    serializer_class = NfcTagMemorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['nfc_tag', 'memory']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show NFC tag memories needed for each role.
        """
        if self.request.user.is_superuser:
            return NfcTagMemory.objects.all()
        elif self.request.user.groups.filter(name='Trainers').exists():
            return NfcTagMemory.objects.filter(nfc_tag__user=self.request.user)
        else:
            return NfcTagMemory.objects.none()

    def create(self, request, *args, **kwargs):
        nfc_tag_id = request.data.get('nfc_tag_id')
        memory = request.data.get('memory')

        if not nfc_tag_id:
            return Response({"error": "NFC Tag ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nfc_tag = NfcTag.objects.get(pk=nfc_tag_id)
        except NfcTag.DoesNotExist:
            return Response({"error": "Invalid NFC Tag ID."}, status=status.HTTP_400_BAD_REQUEST)

        nfc_tag_memory = NfcTagMemory.objects.create(
            nfc_tag=nfc_tag,
            memory=memory
        )

        serializer = self.get_serializer(nfc_tag_memory, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        