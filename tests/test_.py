import django_base
from django_base import version

from unittest import TestCase


class Test_django_base(TestCase):
    def test_version(self):
        self.assertTrue(version.__version__)
        self.assertTrue(version.__version_tuple__)
