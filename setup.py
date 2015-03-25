from distutils.core import setup

with open("README.md") as f:
    README = f.read()

setup(
    name = "django-serverauth",
    version = "1",
    packages = ["serverauth"],
    author = "btidor",
    author_email = "btidor@mit.edu",
    url = "https://github.com/btidor/django-serverauth",
    description = "Middleware for server-mediated authentication",
    long_description = README,
    license = "LICENSE",

    keywords = ["django", "shibboleth", "client certificate", "remote_user"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
