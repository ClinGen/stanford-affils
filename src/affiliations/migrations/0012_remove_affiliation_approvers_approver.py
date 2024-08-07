# Generated by Django 5.0.7 on 2024-07-26 23:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("affiliations", "0011_alter_coordinator_affiliation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="affiliation",
            name="approvers",
        ),
        migrations.CreateModel(
            name="Approver",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("approver_name", models.CharField()),
                (
                    "affiliation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approvers",
                        to="affiliations.affiliation",
                    ),
                ),
            ],
        ),
    ]
