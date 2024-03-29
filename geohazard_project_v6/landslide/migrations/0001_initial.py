# Generated by Django 3.2.7 on 2023-06-30 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import map_auxiliary.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('suscep_level', models.CharField(choices=[('N/A', 'N/A'), ('Level 1', 'Level 1'), ('Level 2', 'Level 2'), ('Level 3', 'Level 3')], default='N/A', max_length=50, unique=True, verbose_name='Response Level')),
                ('suscep_info', models.TextField(verbose_name='Response Level Description')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='landslide_levels', to=settings.AUTH_USER_MODEL, verbose_name='Admin')),
            ],
        ),
        migrations.CreateModel(
            name='Markers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('Alegria', 'Alegria'), ('Bagacay', 'Bagacay'), ('Baluntay', 'Baluntay'), ('Datal Anggas', 'Datal Anggas'), ('Domolok', 'Domolok'), ('Kawas', 'Kawas'), ('Ladol', 'Ladol'), ('Maribulan', 'Maribulan'), ('Pag-Asa', 'Pag-Asa'), ('Paraiso', 'Paraiso'), ('Poblacion', 'Poblacion'), ('Spring', 'Spring'), ('Tokawal', 'Tokawal')], default='Alegria', max_length=50, unique=True)),
                ('level', models.CharField(choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High'), ('Very High', 'Very High')], max_length=50, verbose_name='Risk Level')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='landslide_marker_imgs')),
                ('info', models.TextField()),
            ],
            options={
                'verbose_name': 'Landslide Marker',
                'verbose_name_plural': 'Landslide Markers',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Procedures',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('procedure_name', models.CharField(max_length=50, unique=True)),
                ('procedure_content', models.TextField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landslide.level', verbose_name='Response Levels')),
            ],
            options={
                'verbose_name': 'Landslide Procedure',
                'verbose_name_plural': 'Landslide Procedures',
                'ordering': ['procedure_name'],
            },
        ),
        migrations.CreateModel(
            name='Guidelines',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('alert_level', models.CharField(max_length=50, unique=True, verbose_name='Title')),
                ('alert_level_guide', models.TextField(verbose_name='Content')),
                ('date_published', models.DateField(default=django.utils.timezone.now)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landslide.level', verbose_name='Response Levels')),
            ],
            options={
                'verbose_name': 'Landslide Guidelines',
                'verbose_name_plural': 'Landslide Guidelines',
                'ordering': ['date_published'],
            },
        ),
        migrations.CreateModel(
            name='Choropleth',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('low_risk_map', models.FileField(help_text="Note: Make sure you uploaded the correct 'Low Risk Map' file before confirming changed.", storage=map_auxiliary.utils.OverwriteStorage(location='choropleth_storage'), upload_to=map_auxiliary.utils.LandslideFileRename.rename_to_low, verbose_name='Low Risk Map')),
                ('mod_risk_map', models.FileField(help_text="Note: Make sure you uploaded the correct 'Low Risk Map' file before confirming changed.", storage=map_auxiliary.utils.OverwriteStorage(location='choropleth_storage'), upload_to=map_auxiliary.utils.LandslideFileRename.rename_to_mod, verbose_name='Low Risk Map')),
                ('high_risk_map', models.FileField(help_text="Note: Make sure you uploaded the correct 'Low Risk Map' file before confirming changed.", storage=map_auxiliary.utils.OverwriteStorage(location='choropleth_storage'), upload_to=map_auxiliary.utils.LandslideFileRename.rename_to_high, verbose_name='Low Risk Map')),
                ('very_high_risk_map', models.FileField(help_text="Note: Make sure you uploaded the correct 'Low Risk Map' file before confirming changed.", storage=map_auxiliary.utils.OverwriteStorage(location='choropleth_storage'), upload_to=map_auxiliary.utils.LandslideFileRename.rename_to_very_high, verbose_name='Low Risk Map')),
                ('confirm_map', models.BooleanField(default=False, help_text="(Click on Checkbox) We recommend to 'double-check' the uploaded file first, before confirming change.", verbose_name='Confirm Map Changes?')),
                ('date_changed', models.DateTimeField(default=django.utils.timezone.now)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='landslide_choropleths', to=settings.AUTH_USER_MODEL, verbose_name='Admin')),
            ],
            options={
                'verbose_name': 'Landslide Choropleth',
                'verbose_name_plural': 'Landslide Choropleths',
            },
            bases=(models.Model, map_auxiliary.utils.LandslideFileRename, map_auxiliary.utils.MapInfo),
        ),
    ]
