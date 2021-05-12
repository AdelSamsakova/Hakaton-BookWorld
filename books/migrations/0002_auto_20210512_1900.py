# Generated by Django 3.1 on 2021-05-12 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='format',
            field=models.ManyToManyField(related_name='formats', through='books.ExtraTableForPrice', to='books.Format'),
        ),
    ]