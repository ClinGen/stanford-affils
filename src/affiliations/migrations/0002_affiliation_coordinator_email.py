# Generated by Django 5.0.7 on 2024-07-23 23:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("affiliations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="affiliation",
            name="coordinator_email",
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
    ]
