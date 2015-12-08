#!/usr/bin/env python
import sys
from mock import patch

import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'cloak',
    ),
    MIDDLEWARE_CLASSES=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'cloak.middleware.CloakMiddleware',
    ],
    SECRET_KEY="123",
)

from django.test.utils import get_runner

django.setup()

TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=1)

failures = test_runner.run_tests(['cloak'])
sys.exit(bool(failures))
