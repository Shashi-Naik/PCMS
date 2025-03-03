# Generated by Django 5.1.4 on 2024-12-12 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_mechanicaldrawingupload_projectname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MechanicalProjectTree',
            fields=[
                ('ProjectID', models.AutoField(primary_key=True, serialize=False)),
                ('ProjectName', models.CharField(max_length=255)),
                ('parentId', models.IntegerField(blank=True, null=True)),
                ('parentName', models.CharField(blank=True, max_length=255, null=True)),
                ('childId', models.IntegerField(blank=True, null=True)),
                ('childName', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_MechanicalProjectTree',
            },
        ),
    ]
