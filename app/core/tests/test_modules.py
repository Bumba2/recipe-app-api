from django.test import TestCase
"""import test case class"""
from django.contrib.auth import get_user_model
"""import get user model helper function that comes with django"""

"""Create test class"""


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@londonappdev.com"
        password = "Testpass123"
        """Calling the create user function on the user manager for our user model
        that we are going to create in a future step."""
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        """run some assertions that check whether our user
        has been created correctly"""
        self.assertEqual(user.email, email)
        """is user.email equal to email?"""
        self.assertTrue(user.check_password(password))
        """is the encrypted password correct?"""

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@LONDONAPPDEV.COM"
        user = get_user_model().objects.create_user(email, "test123")
        """Check whether email is now lower case"""
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            """Anything, what we run in here should raise the ValueError"""
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@londonappdev.com",
            "test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
