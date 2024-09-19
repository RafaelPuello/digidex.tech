from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import NFCTag, NFCTagDesign, NFCTagScan, NFCTagMemory
from .serializers import NFCTagSerializer, NFCTagDesignSerializer, NFCTagScanSerializer, NFCTagMemorySerializer


class NFCTagDesignViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing the types of NFC Tag.
    """

    queryset = NFCTagDesign.objects.all().order_by('id')
    serializer_class = NFCTagDesignSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
    body_fields = ['name', 'description', 'owner']
    meta_fields = ['id']

    def create(self, request, *args, **kwargs):
        """
        Create a new ntag design with the provided name, description, and owner.
        """

        name = request.data.get('name')
        description = request.data.get('description')
        owner = request.data.get('owner')

        if not name:
            return Response({"error": "Name not provided."}, status=status.HTTP_400_BAD_REQUEST)

        design, created = NFCTagDesign.objects.update_or_create(
            name=name,
            defaults={
                'description': description,
                'owner': owner
            }
        )

        serializer = self.get_serializer(design, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class NFCTagViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing NFC Tags.
    """

    queryset = NFCTag.objects.all()
    serializer_class = NFCTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'serial_number'
    body_fields = ['serial_number', 'design']
    meta_fields = ['id']

    def get_queryset(self):
        """
        Filter to only show NFC tags needed for each role.
        """

        if self.request.user.is_superuser:
            return NFCTag.objects.all()
        elif self.request.user.groups.filter(name='Trainers').exists():
            return NFCTag.objects.filter(user=self.request.user)
        else:
            return NFCTag.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Create a new NFC tag with the provided serial number and tag type.
        """

        serial_number = request.data.get('serial_number')
        tag_type_id = request.data.get('tag_type_id')

        if not serial_number:
            return Response({"error": "Serial Number not provided."}, status=status.HTTP_400_BAD_REQUEST)

        if tag_type_id:
            try:
                design = NFCTagDesign.objects.get(pk=tag_type_id)
            except NFCTagDesign.DoesNotExist:
                return Response({"error": "Invalid Tag Type ID."}, status=status.HTTP_400_BAD_REQUEST)

        ntag, created = NFCTag.objects.update_or_create(
            serial_number=serial_number,
            defaults={'design': design}
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
        """
        Filter to only show NFC tag scans needed for each role.
        """

        if self.request.user.is_superuser:
            return NFCTagScan.objects.all()
        elif self.request.user.groups.filter(name='Trainers').exists():
            return NFCTagScan.objects.filter(ntag__user=self.request.user)
        else:
            return NFCTagScan.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Create a new NFC tag scan with the provided NFC tag ID and scan time.
        """

        ntag_id = request.data.get('ntag_id')
        scan_time = request.data.get('scan_time')

        if not ntag_id:
            return Response({"error": "NFC Tag ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ntag = NFCTag.objects.get(pk=ntag_id)
        except NFCTag.DoesNotExist:
            return Response({"error": "Invalid NFC Tag ID."}, status=status.HTTP_400_BAD_REQUEST)

        ntag_scan = NFCTagScan.objects.create(
            ntag=ntag,
            scan_time=scan_time
        )

        serializer = self.get_serializer(ntag_scan, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NFCTagMemoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing an NFC Tag's EEPROM.
    """

    queryset = NFCTagMemory.objects.all()
    serializer_class = NFCTagMemorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uuid'
    body_fields = ['ntag', 'memory']
    meta_fields = ['uuid']

    def get_queryset(self):
        """
        Filter to only show NFC tag memories needed for each role.
        """

        if self.request.user.is_superuser:
            return NFCTagMemory.objects.all()
        elif self.request.user.groups.filter(name='Trainers').exists():
            return NFCTagMemory.objects.filter(ntag__user=self.request.user)
        else:
            return NFCTagMemory.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Create a new NFC tag memory with the provided NFC tag ID and memory contents.
        """

        ntag_id = request.data.get('ntag_id')
        memory = request.data.get('memory')

        if not ntag_id:
            return Response({"error": "NFC Tag ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ntag = NFCTag.objects.get(pk=ntag_id)
        except NFCTag.DoesNotExist:
            return Response({"error": "Invalid NFC Tag ID."}, status=status.HTTP_400_BAD_REQUEST)

        ntag_memory = NFCTagMemory.objects.create(
            ntag=ntag,
            memory=memory
        )

        serializer = self.get_serializer(ntag_memory, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
