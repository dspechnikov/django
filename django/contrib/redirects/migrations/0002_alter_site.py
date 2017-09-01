from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirect',
            name='site',
            field=models.CharField(
                max_length=255,
                blank=True,
                verbose_name='domain'
            )
        ),
        migrations.RenameField(
            model_name='redirect',
            old_name='site',
            new_name='domain',
        )
    ]
