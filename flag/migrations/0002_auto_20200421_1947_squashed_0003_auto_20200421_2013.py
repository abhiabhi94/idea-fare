# Generated by Django 3.0.4 on 2020-04-21 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    # replaces = [('flag', '0002_auto_20200421_1947'), ('flag', '0003_auto_20200421_2013')]

    dependencies = [
        ('flag', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='flaggedcontent',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flagged_content_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='flaginstance',
            name='reason',
            field=models.SmallIntegerField(choices=[(1, 'Spam | Exists only to promote a service '), (2, 'Abusive | Intended at promoting hatred'), (3, 'Something Else')], default=1),
        ),
        migrations.AlterField(
            model_name='flaginstance',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flagger', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='flaginstance',
            unique_together={('flagged_content', 'user')},
        ),
    ]