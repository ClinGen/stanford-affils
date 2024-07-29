# Generated by Django 5.0.7 on 2024-07-26 03:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("affiliations", "0010_remove_affiliation_coordinator_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coordinator",
            name="affiliation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="coordinators",
                to="affiliations.affiliation",
            ),
        ),
    ]