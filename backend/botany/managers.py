from ntags.managers import NFCTaggableManager


class UserPlantManager(NFCTaggableManager):
    """
    Custom manager for UserPlant model, extending the abstract NFCTaggableManager.
    """

    def for_user(self, user):
        """
        Get a queryset of UserPlant instances for a specific user.
        """
        return self.filter(box__owner=user)

    def with_nfc_tag(self, user=None):
        """
        Get a queryset of linked object instances with NFC tags,
        optionally filtered by user.
        """
        queryset = super().with_nfc_tag()
        if user:
            queryset = queryset.filter(box__owner=user)
        return queryset

    def without_nfc_tag(self, user=None):
        """
        Get a queryset of linked object instances without NFC tags,
        optionally filtered by user.
        """
        queryset = super().without_nfc_tag()
        if user:
            queryset = queryset.filter(box__owner=user)
        return queryset
