# Generated by Django 5.0.10 on 2025-02-10 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0004_savedsearch"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SavedSearch",
        ),
    ]
