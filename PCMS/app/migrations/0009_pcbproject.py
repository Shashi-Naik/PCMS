# Generated by Django 5.1.4 on 2025-01-03 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_mechproject'),
    ]

    operations = [
        migrations.CreateModel(
            name='PCBProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProjectId', models.CharField(max_length=255, null=True)),
                ('ProjectName', models.CharField(max_length=255, null=True)),
                ('ParentId', models.CharField(max_length=255)),
                ('ParentName', models.CharField(max_length=255)),
                ('ChildId', models.CharField(max_length=255)),
                ('ChildName', models.CharField(max_length=255)),
                ('Path', models.CharField(max_length=255)),
                ('PCBName', models.CharField(max_length=255)),
                ('PCBId', models.CharField(max_length=255)),
                ('Reamrks', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_PCBProject',
            },
        ),
    ]
