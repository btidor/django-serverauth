from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission

class ServerAuthBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``ServerAuthMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """

    # Create a User object if not already in the database?
    create_unknown_user = True

    def authenticate(self, request):
        """
        This method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        username = self.extract_username(request)

        UserModel = get_user_model()

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = UserModel._default_manager.get_or_create(**{
                UserModel.USERNAME_FIELD: username
            })
            if created:
                user = self.configure_user(user, request)
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass
        return user

    def extract_username(self, request):
        """
        Extracts the username of the logged-in user from the request.
        """
        username = request.META[settings.SERVER_USER]
        username = username.lower()

        if settings.SERVER_STRIP_SUFFIX:
            suffix = settings.SERVER_STRIP_SUFFIX
            if username.endswith(suffix):
                username = username[:-len(suffix)]

        return username

    def configure_user(self, user, request):
        """
        Configures a user after creation and returns the updated user. Extracts
        variables from the request (if present) and sets them on ther user
        object according to the SERVER_ATTRIBUTES dictionary.
        """
        for server_var, user_attr in settings.SERVER_ATTRIBUTES.iteritems():
            if server_var in request.META:
                setattr(user, user_attr, request.META[server_var])
        user.save()
        return user
