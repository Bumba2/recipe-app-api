from django.test import TestCase, Client
"""Client:testclient, which allows us to make test requests
to our application in our unit tests"""
from django.contrib.auth import get_user_model
from django.urls import reverse
"""allows us to generate URLs for our Django admin page"""


class AdminSiteTests(TestCase):

    """setUp function is a function that is ran before
    every test that we run. Sometimes there are setup
    tasks that need to be done before every test in
    our testcase class."""
    def setUp(self):

        """setUp consists of creating our testclient,
        add a new user that we can use to test, we
        are gonna make sure this user is logged into
        our client, and finally we are going to create
        a regular user that is not authenticated or that
        we can use to list in our admin page."""
        self.client = Client()
        """=>sets to self a client variable, which make it
        accessible in the other test a client variable"""
        self.admin_user = get_user_model().objects.create_superuser(
            email="admn@londonappdev.com",
            password="password123"
        )
        self.client.force_login(self.admin_user)
        """=>What this does is that it uses the client helper function
        that allows you to log a user in (to the client) with the Django
        authentification and this really helps a lot easier to write
        because it means we don't have to manually log the user in, we
        can just use this helper function."""
        self.user = get_user_model().objects.create_user(
            email="test@londonappdev.com",
            password="password123",
            name="Test user full name"
        )
        """=>spare user which we can use for testing listing and things
        like that."""

    """Test that our users are listed in our Django admin. We need to add
    a test for this because we need to slightly customize the Django admin
    to work with our custom user model."""
    """The default user model expects a username and as such the default
    Django admin expects for the user model a username which we dont
    have. We just have the email address, so we need to make a few small
    changes to our admin.py file just to make it support our custom
    user model."""

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse("admin:core_user_changelist")
        """Creating the url first using the reverse helper function
        using it like 'app you are going for : url'
        => These urls are defined in the Django admin documentation.
        It will generate the url for our list user page."""

        res = self.client.get(url)
        """res=> response. This will use our test client to make a
        http GET on the URL we have found here."""

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        """The assert Contains assertions is a Django custom assertion
        that will check that our response here contains a certain
        item. It also checks whether the HTTP-Response was HTTP 200
        and that it looks into the actual content/output of the res object
        and to check for the contents (second parameter)"""

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        """generates an url like this: /admin/user/core/user-Id
        => args adds the correct user-Id"""
        res = self.client.get(url)
        """=>Perform a HTTP-GET on the url"""

        self.assertEqual(res.status_code, 200)
        """=> checks whether the status code for our response that the
        client give is HTTP 200 (OK)."""

    """Check whether the user add page renders correctly"""
    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
