import time
"""=>default Python module that we can use to make
our applications sleep for a few seconds in between
each database check."""
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
"""1. connections module: we can use it to test if the
database connection is available. 2. OperationalError
is the exception that django will throw, if the database
is not available. 3. BaseCommand is the class that we
need to build on in order to create our custom command."""


class Command(BaseCommand):
    """Django command to pause execution until database
    is available."""

    """handle function. *args and **options allows us to passing
    in custom arguments and options to our managements command
    so if we want customize the wait time for example we could
    do that as an option. All we are gonna do here is check if
    the database is available and once it is available we are
    going to cleanly exit, so that which ever command we want to
    run next, we can run knowing that the database is ready."""
    def handle(self, *args, **options):
        """print things out to the screen during the management
        command:"""
        self.stdout.write("Waiting for database...")
        db_conn = None
        """During the database is not connected (db_conn is a falsy
        value like None, false or null), try and set db.conn to the
        database connection. If the connection is unavailable, django
        raises the operational error. Then it output that the database
        is currently unavailable and that we are waiting for one second
        and then we go asleep for one second (it pauses the execution
        for a second). And then it will try again and start from the
        beginning and it will continue this process until the database
        is finally available in which case it will just exit."""
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
