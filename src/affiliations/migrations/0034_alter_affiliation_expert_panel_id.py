# Generated by Django 5.1.2 on 2024-10-13 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("affiliations", "0033_merge_20240927_1839"),
    ]

    operations = [
        migrations.AlterField(
            model_name="affiliation",
            name="expert_panel_id",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Expert Panel ID"
            ),
        ),
    ]