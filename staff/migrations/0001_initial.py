# Generated by Django 3.2.8 on 2021-10-12 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requested',
            fields=[
                ('request_pk', models.AutoField(primary_key=True, serialize=False)),
                ('request_number', models.CharField(max_length=40)),
                ('request_service', models.CharField(max_length=40)),
                ('request_reason', models.CharField(max_length=100)),
                ('request_date', models.DateField(auto_now_add=True)),
                ('comp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.comp')),
            ],
        ),
    ]