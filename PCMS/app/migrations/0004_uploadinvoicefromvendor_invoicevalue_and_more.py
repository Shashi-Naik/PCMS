# Generated by Django 5.0.2 on 2024-11-11 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_createcustomer_bankacc_createcustomer_branch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadinvoicefromvendor',
            name='InvoiceValue',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadinvoicefromvendor',
            name='CostPerunit',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='uploadinvoicefromvendor',
            name='TotalValue',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
