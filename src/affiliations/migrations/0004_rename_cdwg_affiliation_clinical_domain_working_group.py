# Generated by Django 5.0.7 on 2024-07-24 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("affiliations", "0003_rename_family_affiliation_cdwg"),
    ]

    operations = [
        migrations.RenameField(
            model_name="affiliation",
            old_name="cdwg",
            new_name="clinical_domain_working_group",
        ),
    ]
