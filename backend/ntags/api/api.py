from rest_framework.routers import DefaultRouter
from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from ..models import NFCTag
from .serializers import NFCTagSerializer


class NFCTagAPIViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, and linking NFC tags.
    """
    queryset = NFCTag.objects.all()
    serializer_class = NFCTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'uid'

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
        uid = request.data.get('uid')

        if not uid:
            return Response({"error": "Serial Number not provided."}, status=status.HTTP_400_BAD_REQUEST)

        nfc_tag, created = NFCTag.objects.update_or_create(
            uid=uid
        )

        serializer = self.get_serializer(nfc_tag, context={'request': request})
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


router = DefaultRouter()
router.register(r'nfc-tags', NFCTagAPIViewSet, basename='nfc-tag')  # noqa