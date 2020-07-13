# Generated by Django 3.0.7 on 2020-07-13 06:06

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0015_auto_20190724_1210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='huc2',
            old_name='huc2_id',
            new_name='huc_id',
        ),
        migrations.RenameField(
            model_name='huc4',
            old_name='huc4_id',
            new_name='huc_id',
        ),
        migrations.RenameField(
            model_name='huc4',
            old_name='huc2',
            new_name='lower_huc',
        ),
        migrations.RenameField(
            model_name='huc6',
            old_name='huc6_id',
            new_name='huc_id',
        ),
        migrations.RenameField(
            model_name='huc6',
            old_name='huc4',
            new_name='lower_huc',
        ),
        migrations.RenameField(
            model_name='huc8',
            old_name='huc8_id',
            new_name='huc_id',
        ),
        migrations.RenameField(
            model_name='huc8',
            old_name='huc6',
            new_name='lower_huc',
        ),
        migrations.AlterField(
            model_name='huc6',
            name='geometry',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326),
        ),
        migrations.AlterField(
            model_name='huc8',
            name='geometry',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326),
        ),
    ]