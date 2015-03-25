# django-serverauth
_Middleware for server-mediated authentication (e.g. client certificate, Shibboleth)_

The `django-serverauth` module allows Django websites to accept authentication schemes that are provided by the web server, such as TLS client certificates and Shibboleth SSO. Features that go over and above Django's built-in `REMOTE_USER` support include:

  * populating the User object with server-provided metadata like name and email address;
  * only requiring the server to protect one URL (`/accounts/login/`) rather than the entire site; and
  * optional suffix-stripping (to convert `john@example.org` to `john`).

## Usage
1. **Install `django-serverauth`**

    ```
    pip install --upgrade  git+https://github.com/btidor/django-serverauth.git
    ```

2. **Configure the Web Server**

  The server must be configured to request authentication for the login URL, which is `/accounts/login/` by default. The commands will vary by server type and authentication method, but one example is shown below:

    ```
    location = /accounts/login/ {
        shib_request /shibauthorizer;
        try_files $uri @app;
    }
    ```

3. **Enable `django-serverauth`**

  In `settings.py`:

    ```
    MIDDLEWARE_CLASSES = (
        '...',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'serverauth.middleware.ServerAuthMiddleware',
        '...',
    )

    AUTHENTICATION_BACKENDS = (
        'serverauth.backends.ServerAuthBackend',
    )
    ```

4. **Configure `django-serverauth`**

  Determine which environment variables the server sets to indicate that a user is logged in. A sample configuration is:

    ```
    SERVER_USER = 'REMOTE_USER'
    SERVER_STRIP_SUFFIX = '@mit.edu'  # False to disable
    SERVER_ATTRIBUTES = {
        'SSL_CLIENT_S_DN_CN': 'first_name',
        'SSL_CLIENT_S_DN_Email': 'email',
        # Environment Variable => User object attribute
    }
    ```

## Contributions
This module is based on Django's `REMOTE_USER` support and Brown University's [django-shibboleth-remoteuser](https://github.com/Brown-University-Library/django-shibboleth-remoteuser).
