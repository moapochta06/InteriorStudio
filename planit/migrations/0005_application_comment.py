# Generated by Django 5.0.7 on 2024-11-10 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planit', '0004_alter_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
    ]
