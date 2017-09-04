from django.apps import apps as django_apps
from django.db import migrations, models


def migrate_site_domains(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    try:
        Site = apps.get_model('sites', 'Site')
    except LookupError:
        return

    Redirect = apps.get_model('redirects', 'Redirect')
    for r in Redirect.objects.using(db_alias).all():
        if r.site_id:
            site = Site.objects.get(id=r.site_id)

            r.domain = site.domain
            r.save()


class Migration(migrations.Migration):

    dependencies = [
        ('redirects', '0001_initial'),
    ]

    if django_apps.is_installed('django.contrib.sites'):
        dependencies.append(
            ('sites', '0002_alter_domain_unique'),
        )

    operations = [
        migrations.AddField(
            model_name='redirect',
            name='domain',
            field=models.CharField(
                blank=True,
                help_text='If set, redirect requests from this domain only.',
                max_length=255,
                verbose_name='domain'
            ),
        ),

        migrations.RunPython(migrate_site_domains, migrations.RunPython.noop),

        migrations.RemoveField(
            model_name='redirect',
            name='site_id'
        ),
        migrations.AlterUniqueTogether(
            name='redirect',
            unique_together=('old_path', 'domain')
        ),
    ]
