from django.contrib.admin import widgets

from django import forms

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.options import get_ul_class
from django.contrib.redirects.models import Redirect
from django.utils.translation import gettext_lazy as _


class RedirectForm(forms.ModelForm):
    if apps.is_installed('django.contrib.sites'):
        from django.contrib.sites.models import Site

        site = forms.ModelChoiceField(
            queryset=Site.objects.all(),
            to_field_name='domain',
            empty_label='Any',
            widget=widgets.AdminRadioSelect(attrs={
                'class': get_ul_class(admin.VERTICAL),
            }),
            label=_('Site'),
            help_text=_('If domain is not set, redirect from this site.'),
            required=False,
        )


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    form = RedirectForm

    list_display = ('old_path', 'new_path', 'domain')
    list_filter = ('domain',)
    search_fields = ('domain', 'old_path', 'new_path')

    def get_fieldsets(self, request, obj=None):
        redirect_from_fields = ['old_path', 'domain']

        if apps.is_installed('django.contrib.sites'):
            redirect_from_fields.append('site')

        return (
            (_('Source'), {
                'fields': redirect_from_fields
            }),
            (_('Destination'), {
                'fields': ('new_path',)
            }),
        )
