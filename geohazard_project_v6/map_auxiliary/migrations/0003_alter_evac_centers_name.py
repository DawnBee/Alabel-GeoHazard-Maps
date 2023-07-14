# Generated by Django 3.2.7 on 2023-07-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_auxiliary', '0002_alter_evac_centers_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evac_centers',
            name='name',
            field=models.CharField(choices=[('Municipal Gym', 'Municipal Gym'), ('Purok 1 (Baluntay)', 'Purok 1 (Baluntay)'), ('Alabel Central Elem. School', 'Alabel Central Elem. School'), ('Bagacay Gym', 'Bagacay Gym'), ('Alegria Covered Court', 'Alegria Covered Court'), ('Purok Kawayan (Bagacay)', 'Purok Kawayan (Bagacay)')], max_length=100, unique=True),
        ),
    ]