from unittest import skipIf

from django.contrib.admin import AdminSite
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.redirects.admin import RedirectAdmin

from django.apps import apps
from django.contrib.redirects import admin
from django.contrib.redirects.models import Redirect
from django.forms import modelform_factory
from django.test import TestCase, modify_settings, RequestFactory


class RedirectFormTests(TestCase):
    def setUp(self):
        self.form_class = modelform_factory(Redirect, form=admin.RedirectForm, fields='__all__')

    @skipIf(not apps.is_installed('django.contrib.sites'),
            'django.contrib.sites is not installed')
    def test_site_overrides_empty_domain(self):
        from django.contrib.sites.models import Site
        site = Site.objects.create(domain='site.loc', name='site')
        form = self.form_class(data={
            'old_path': '/old/',
            'site': site.domain
        })

        form.save()

        self.assertTrue(
            Redirect.objects.get(domain=site.domain, old_path='/old/')
        )

    @skipIf(not apps.is_installed('django.contrib.sites'),
            'django.contrib.sites is not installed')
    def test_non_empty_domain_overrides_site(self):
        from django.contrib.sites.models import Site
        site = Site.objects.create(domain='site.loc', name='site')
        form = self.form_class(data={
            'old_path': '/old/',
            'domain': 'test.loc',
            'site': site.domain
        })

        form.save()

        self.assertTrue(
            Redirect.objects.get(domain='test.loc', old_path='/old/')
        )

    @modify_settings(INSTALLED_APPS={'remove': 'django.contrib.sites'})
    def test_no_sites_framework(self):
        form = self.form_class(data={
            'old_path': '/old/',
            'site': 'site.loc'
        })

        form.save()

        self.assertTrue(
            Redirect.objects.get(domain='', old_path='/old/')
        )


class RedirectAdminTests(TestCase):
    def test_site_field_enabled(self):
        ma = RedirectAdmin(Redirect, AdminSite())
        request = RequestFactory().get('/')

        fields = flatten_fieldsets(ma.get_fieldsets(request))

        self.assertIn('site', fields)

    @modify_settings(INSTALLED_APPS={'remove': 'django.contrib.sites'})
    def test_no_site_field(self):
        ma = RedirectAdmin(Redirect, AdminSite())
        request = RequestFactory().get('/')

        fields = flatten_fieldsets(ma.get_fieldsets(request))

        self.assertNotIn('site', fields)
