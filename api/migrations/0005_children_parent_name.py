# Generated by Django 4.2.2 on 2023-06-13 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_children_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='children',
            name='parent_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]