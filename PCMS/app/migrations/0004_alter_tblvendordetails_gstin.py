# Generated by Django 5.0.2 on 2024-10-31 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_project_code1_tblproject_project_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblvendordetails',
            name='gstin',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
