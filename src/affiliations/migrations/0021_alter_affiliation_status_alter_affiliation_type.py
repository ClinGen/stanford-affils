# Generated by Django 5.1 on 2024-08-13 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("affiliations", "0020_alter_affiliation_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="affiliation",
            name="status",
            field=models.CharField(
                choices=[
                    ("APPLYING", "Applying"),
                    ("ACTIVE", "Active"),
                    ("INACTIVE", "Inactive"),
                    ("RETIRED", "Retired"),
                    ("ARCHIVED", "Archived"),
                ],
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="affiliation",
            name="type",
            field=models.CharField(
                choices=[
                    ("VCEP", "Variant Curation Expert Panel"),
                    ("GCEP", "Gene Curation Expert Panel"),
                    ("INDEPENDENT_CURATION", "Independent Curation Group"),
                ],
                verbose_name="type",
            ),
        ),
    ]