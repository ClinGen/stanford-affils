# Generated by Django 5.0.7 on 2024-07-29 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("affiliations", "0015_rename_submitter_id_submitter_clinvar_submitter_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="affiliation",
            name="curation_panel_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]