from django.conf import settings
from django.contrib import auth
from django.contrib.auth import load_backend
from django.core.exceptions import ImproperlyConfigured

from serverauth.backends import ServerAuthBackend

class ServerAuthMiddleware(object):
    """
    Middleware for utilizing Web-server-provided authentication. Based on
    django.contrib.auth.RemoteUserMiddleware, but enables other fields in the
    user profile to be filled out from metadata, and only requires
    authentication-related environment variables to be set on the login page.
    """

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django server auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the ServerAuthMiddleware class.")

        if settings.SERVER_USER not in request.META:
            # If the required variable isn't  available, don't touch the request:
            # the user may already be logged in via a session.
            return

        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.get_username() == self.extract_username(request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(request=request)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def extract_username(self, request):
        """
        Asks the backend to parse the username out of the request."
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        return backend.extract_username(request)

    def _remove_invalid_user(self, request):
        """
        Removes the current authenticated user in the request which is invalid
        but only if the user is authenticated via the ServerAuthBackend.
        """
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ''))
        except ImportError:
            # backend failed to load
            auth.logout(request)
        else:
            if isinstance(stored_backend, ServerAuthBackend):
                auth.logout(request)
