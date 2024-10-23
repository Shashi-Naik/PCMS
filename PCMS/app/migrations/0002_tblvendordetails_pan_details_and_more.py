# Generated by Django 5.0.2 on 2024-10-22 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblvendordetails',
            name='Pan_details',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblvendordetails',
            name='Tally_ledger_creation',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tblvendordetails',
            name='gstin',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='tblvendordetails',
            name='vendor_code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterModelTable(
            name='tblvendordetails',
            table=None,
        ),
    ]
