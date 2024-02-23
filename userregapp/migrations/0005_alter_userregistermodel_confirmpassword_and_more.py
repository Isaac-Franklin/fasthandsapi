# Generated by Django 4.2.7 on 2024-02-23 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userregapp', '0004_remove_userregistermodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistermodel',
            name='ConfirmPassword',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userregistermodel',
            name='Email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='userregistermodel',
            name='Fullname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userregistermodel',
            name='Location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userregistermodel',
            name='NIN',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userregistermodel',
            name='Password',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userregistermodel',
            name='PhoneNumber',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userregistermodel',
            name='Skill',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]