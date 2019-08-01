from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.core.exceptions import FieldError
from django.core.validators import validate_email
from ...views import login

class Command(BaseCommand):
    args = '[USERNAME_FIELD value]'
    help = 'Login as a user using a temporary URL'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('identifier', nargs='?')

    def handle(self, *args, **options):
        """
        With no arguments, find the first user in the system with the
        is_superuser or is_staff flag set to true, or just the first user in
        the system period.

        With a single argument, look for the user with that value as the
        USERNAME_FIELD value.

        When a user is found, print out a URL slug you can paste into your
        browser to login as the user.
        """
        user_model = get_user_model()

        identifier = options['identifier']

        if not identifier:
            # find the first superuser, or staff member or user
            filters = [{"is_superuser": True}, {"is_staff": True}, {}]
            user = None
            for f in filters:
                try:
                    user = user_model._default_manager.filter(**f).order_by("pk").first()
                    if user:
                        break
                except FieldError as e:
                    pass

            if user is None:
                raise CommandError("No users found!")
        else:
            # find the user with the email field or USERNAME_FIELD equal to the command line
            # argument
            try:
                user = user_model._default_manager.filter(pk=identifier).first()
            except:
                user = None

            if not user:
                user = user_model._default_manager.filter(email=identifier).order_by("-is_active").first()
                if not user:
                    try:
                        user = user_model._default_manager.get_by_natural_key(identifier)
                    except user_model.DoesNotExist as e:
                        raise CommandError("The user does not exist")

        signer = TimestampSigner()
        signature = signer.sign(str(user.pk))

        self.stdout.write(reverse(login, args=(signature,)))
