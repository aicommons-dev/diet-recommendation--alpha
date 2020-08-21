# Generated by Django 3.0.5 on 2020-08-19 14:52

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20)),
                ('value', models.IntegerField()),
                ('category', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Calorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_class', models.CharField(max_length=50)),
                ('measurement', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=50)),
                ('calories', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Foodservoire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_class', models.CharField(max_length=50)),
                ('nutrients_present', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Carbohydrates'), (2, 'Protein'), (3, 'Vitamins'), (4, 'Fats and Oil'), (5, 'Mineral'), (6, 'Water')], max_length=11)),
                ('nutrients_absent', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Carbohydrates'), (2, 'Protein'), (3, 'Vitamins'), (4, 'Fats and Oil'), (5, 'Mineral'), (6, 'Water')], max_length=11)),
                ('balanced', models.BooleanField()),
            ],
        ),
    ]