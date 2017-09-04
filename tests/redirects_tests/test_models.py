from django.contrib.redirects.models import Redirect
from django.test import TestCase


class RedirectTests(TestCase):
    def test_str_representation(self):
        r = Redirect.objects.create(
            domain='test.loc',
            old_path='/initial',
            new_path='/new_target'
        )

        self.assertEqual(str(r), "test.loc/initial ---> /new_target")
