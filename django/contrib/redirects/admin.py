from django.contrib.admin import widgets

from django import forms

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.options import get_ul_class
from django.contrib.redirects.models import Redirect
from django.utils.translation import gettext_lazy as _


class RedirectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if apps.is_installed('django.contrib.sites'):
            from django.contrib.sites.models import Site

            self.fields['site'] = forms.ModelChoiceField(
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

    def save(self, commit=True):
        self.full_clean()

        if apps.is_installed('django.contrib.sites'):
            site = self.cleaned_data.get('site')

            self.instance.domain = self.instance.domain or getattr(site, 'domain', '')

        return super().save(commit=commit)


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    form = RedirectForm

    list_display = ('old_path', 'new_path', 'domain')
    list_filter = ('domain',)
    search_fields = ('domain', 'old_path', 'new_path')

    def get_fieldsets(self, request, obj=None):
        source_fields = ['old_path', 'domain']

        if apps.is_installed('django.contrib.sites'):
            source_fields.append('site')

        return (
            (_('Source'), {
                'fields': source_fields
            }),
            (_('Destination'), {
                'fields': ('new_path',)
            }),
        )

    def get_form(self, request, obj=None, **kwargs):
        kwargs['fields'] = ('old_path', 'domain', 'new_path')

        return super().get_form(request, obj, **kwargs)
