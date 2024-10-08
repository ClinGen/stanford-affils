# Generated by Django 5.1 on 2024-08-13 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("affiliations", "0021_alter_affiliation_status_alter_affiliation_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="affiliation",
            name="clinical_domain_working_group",
            field=models.CharField(
                choices=[
                    ("NONE", "None"),
                    ("CARDIOVASCULAR", "Cardiovascular"),
                    ("HEARING_LOSS", "Hearing Loss"),
                    ("HEMOSTASIS_THROMBOSIS", "Hemostasis/Thrombosis"),
                    ("HEREDITARY_CANCER", "Hereditary Cancer"),
                    ("IMMUNOLOGY", "Immunology"),
                    ("INBORN_ERR_METABOLISM", "Inborn Errors of Metabolism"),
                    ("KIDNEY_DISEASE", "Kidney Disease"),
                    ("NEURODEVELOPMENTAL_DISORDER", "Neurodevelopmental Disorders"),
                    ("NEUROLOGICAL_DISORDERS", "Neurological Disorders"),
                    ("OCULAR", "Ocular"),
                    ("OTHER", "Other"),
                    ("PULMONARY", "Pulmonary"),
                    ("RASOPATHY", "RASopathy"),
                    ("RHEUMA_AUTO_DISEASE", "Rheumatologic Autoimmune Disease"),
                    ("SKELETAL_DISORDERS", "Skeletal Disorders"),
                    ("SOMATIC_CANCER", "Somatic Cancer"),
                ],
                verbose_name="CDWG",
            ),
        ),
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
                verbose_name="Status",
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
                verbose_name="Type",
            ),
        ),
    ]
