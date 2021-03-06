# Generated by Django 2.0.3 on 2018-04-19 17:28

from django.db import migrations


GROUPS = [
    'Core',
    'Editors',
    'Writers',
    'Reviewers',
    'Audio Reviewers',
]

def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    groups = [Group(name=name) for name in GROUPS]
    Group.objects.bulk_create(groups)


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=groups).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]
