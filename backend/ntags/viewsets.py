from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from wagtail.admin.panels import TabbedInterface, FieldPanel, ObjectList
from wagtail.snippets.views.snippets import SnippetViewSet

from base.widgets import ContentObjectChooserWidget
from .models import NFCTag, NFCTagScan
from .serializers import NFCTagSerializer, NFCTagScanSerializer


class NFCTagViewSet(viewsets.ModelViewSet):

    queryset = NFCTag.objects.all()
    serializer_class = NFCTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'serial_number'
    body_fields = ['serial_number', 'design']
    meta_fields = ['id']

    def get_queryset(self):
        return NFCTag.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new NFC tag with the provided serial number and tag type.
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
            ntag = NFCTag.objects.get(pk=ntag_id)
        except NFCTag.DoesNotExist:
            return Response({"error": "Invalid NFC Tag ID."}, status=status.HTTP_400_BAD_REQUEST)

        ntag_scan = NFCTagScan.objects.create(
            ntag=ntag,
            scan_time=scan_time
        )

        serializer = self.get_serializer(ntag_scan, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NFCTagSnippetViewSet(SnippetViewSet):

    model = NFCTag
    icon = "nfc-icon"
    menu_label = "NFC Tags"
    menu_name = "ntags"
    menu_order = 130
    copy_view_enabled = False
    list_filter = {"nfc_tag_type": ["exact"], "label": ["icontains"]}
    list_display = ["label", "nfc_tag_type", "serial_number"]
    list_per_page = 25
    admin_url_namespace = "nfc_tags"
    base_url_path = "nfc-tags"
    add_to_admin_menu = True

    shared_panels = [
        FieldPanel("label"),
        FieldPanel("content_type"),
        FieldPanel(
            'object_id',
            widget=ContentObjectChooserWidget
            ),
    ]
    private_panels = [
        FieldPanel("nfc_tag_type"),
        FieldPanel("active"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(shared_panels, heading='Details'),
            ObjectList(private_panels, heading='Admin only', permission="superuser"),
        ]
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is None:
            qs = self.model.objects.all()

        user = request.user
        if user.is_superuser:
            return qs
        else:
            return qs.filter(user=user)
