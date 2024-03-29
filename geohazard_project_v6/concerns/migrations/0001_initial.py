# Generated by Django 3.2.7 on 2023-06-30 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location', models.CharField(choices=[('Alegria', 'Alegria'), ('Bagacay', 'Bagacay'), ('Baluntay', 'Baluntay'), ('Datal Anggas', 'Datal Anggas'), ('Domolok', 'Domolok'), ('Kawas', 'Kawas'), ('Ladol', 'Ladol'), ('Maribulan', 'Maribulan'), ('Pag-Asa', 'Pag-Asa'), ('Paraiso', 'Paraiso'), ('Poblacion', 'Poblacion'), ('Spring', 'Spring'), ('Tokawal', 'Tokawal')], default='Alegria', max_length=50)),
                ('post_img', models.ImageField(blank=True, null=True, upload_to='post_images', verbose_name='Image (Optional)')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('is_approved', models.BooleanField(default=False, help_text="Post will be displayed in the community after it's approved.", verbose_name='Approve concern?')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('flag_react', models.ManyToManyField(blank=True, related_name='concern_posts_flagged', to=settings.AUTH_USER_MODEL)),
                ('upvote_react', models.ManyToManyField(blank=True, related_name='concern_posts_upvoted', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='GuestPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.CharField(blank=True, default='Anonymous User', max_length=20, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(choices=[('Alegria', 'Alegria'), ('Bagacay', 'Bagacay'), ('Baluntay', 'Baluntay'), ('Datal Anggas', 'Datal Anggas'), ('Domolok', 'Domolok'), ('Kawas', 'Kawas'), ('Ladol', 'Ladol'), ('Maribulan', 'Maribulan'), ('Pag-Asa', 'Pag-Asa'), ('Paraiso', 'Paraiso'), ('Poblacion', 'Poblacion'), ('Spring', 'Spring'), ('Tokawal', 'Tokawal')], default='Alegria', max_length=50)),
                ('post_img', models.ImageField(blank=True, null=True, upload_to='post_images', verbose_name='Image (Optional)')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('is_approved', models.BooleanField(default=False, help_text="Post will be displayed in the community after it's approved.", verbose_name='Approve concern?')),
                ('flag_react', models.ManyToManyField(blank=True, related_name='concern_guest_posts_flagged', to=settings.AUTH_USER_MODEL)),
                ('upvote_react', models.ManyToManyField(blank=True, related_name='concern_guest_posts_upvoted', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Guest Post',
                'verbose_name_plural': 'Guest Posts',
            },
        ),
        migrations.CreateModel(
            name='CombinedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_post', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='concerns.guestpost')),
                ('post', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='concerns.post')),
            ],
        ),
    ]
