from allauth.account.adapter import DefaultAccountAdapter


class UserAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter for the user model.
    """

    def get_login_redirect_url(self, request):
        """
        Returns the default URL to redirect to after logging in.
        Note that URLs passed explicitly (e.g. by passing along a next GET parameter)
        take precedence over the value returned here.
        """
        return "/dashboard/"

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.
        """
        return False
