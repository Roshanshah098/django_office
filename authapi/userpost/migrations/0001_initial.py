# Generated by Django 5.1 on 2024-08-11 06:40

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Biography')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other', max_length=10)),
                ('address', models.CharField(choices=[('ktm', 'Kathmandu'), ('lat', 'Lalitpur'), ('bat', 'Bhaktapur')], default='ktm', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/')),
                ('favorite_genre', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other', max_length=10)),
                ('address', models.CharField(choices=[('ktm', 'Kathmandu'), ('lat', 'Lalitpur'), ('bat', 'Bhaktapur')], default='ktm', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Post Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Published Date')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Rating')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('tags', models.CharField(blank=True, max_length=100, verbose_name='Tags')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='userpost.author')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_posts', to='userpost.reader')),
            ],
        ),
    ]
