from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
"""1. Allows us mock the behavior from the Django get database function
=> we can simulate the db for being available and not being available
to test our command"""
"""2. => allow us to call the command in our source code"""
"""3. => operational error which django throws when the database
is unavailable. We use this error to simulate the database
being available or not when we run our command."""
"""4. => import our testCase"""

"""Create our testClass"""


class CommanTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        """When an OperationalError is not thrown, then the
        database is available and the command will continue,
        otherwise it is not available."""
        """To setup our test, we are gonna override the
        behavior of the connection handler and we are
        just going to make it return true and not throw
        any exception and therefore our call command
        or our management commands should just continue
        and allow us to continue with the execution flow."""
        """Use the patch to mock our connectionHandler to
        just return true every time it's called"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            """the way we tested the database is available
            in Django is we try and retrieve the default
            database via the ConnectionHandler. The function
            when we retrieve the database is __getitem__ from
            django.db.utils.ConnectionHandler. So we mock
            the behavior from __getitem__ using the patch
            which is assigned as a variable here called gi."""
            """mock the behavior of a function:"""
            gi.return_value = True
            """=>Set up our Test: Whenever this is called during our test execution
            instead of actually before performing whatever behavior
            the item in the patch parentheses does in Django: It
            overwrite it and just replace it with a mock object
            which does two things: 1. It will just return the value
            we specified (here: True) and 2. It allows us to monitor
            how many times it was called and the different calls
            that were made to it."""
            call_command("wait_for_db")
            """=>Test our call command. wait_for_db is the management
            command that we create."""
            self.assertEqual(gi.call_count, 1)
            """=>Test if our __getitem__ has been called once."""

    """Check that the wait for db command will try the database five times
    and then on the sixth time it will be succesfull and it will continue"""
    """adding the patch as a decorator to our function: When you use patch
    as a decorator you can pass in the return_value as part of the function
    call here. It does the same thing as in a with statement, but you put
    it above the test that you are running and then it passes in what is
    the equivalent of the "gi" in the former test as an argument to
    our function. So we need to add the extra argument here for ts (even
    though we are not using it). This mock here replaces the behavior of
    time.sleep and just replaces it with a mock function that returns true.
    That means during our test it will not actually wait the second or
    however long you have it to wait in your code.
    Reason: Speed up the test when you run them because if we are checking
    the database five times then that is five extra seconds that it would
    take to run our tests and we really dont need that slowing down the
    test execution."""
    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db:"""
        """There will be a while-loop that checks to see if the ConnectionHandler
        raises the operational error and if it does: Raise the operational
        error, then it is going to wait a second and then try again. This is
        just so it does not flood the output by trying every microsecond to
        test for the database, so it adds a little delay there and we can
        actually remove that delay by adding the patch."""
        """Using our with patch context manager again:"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            """Instead of adding a return value we are adding a side effect.
            The python unit test mock module has a really useful option where
            you can set a side effect to the function that you are mocking.
            We will make it raise as a side effect five times the operational
            error so that the first five times it tries it can raise the
            operational error and then on the sixth time it's not gonna raise
            the error and then the call should complete."""
            gi.side_effect = [OperationalError] * 5 + [True]
            """=> this means the first five times you call this get item it's
            going to raise the OperationalError and then on the sixth time
            it wont raise the error, it will just return."""
            call_command("wait_for_db")
            """We can check whether it was successful on the sixth time:"""
            self.assertEqual(gi.call_count, 6)
