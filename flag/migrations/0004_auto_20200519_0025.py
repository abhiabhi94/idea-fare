# Generated by Django 3.0.4 on 2020-05-19 00:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flag', '0003_auto_20200423_1704'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flaggedcontent',
            old_name='status',
            new_name='state',
        ),
        migrations.AlterField(
            model_name='flaggedcontent',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flaggedcontent',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flags', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='flaggedcontent',
            name='moderator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flag_moderators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='flaginstance',
            name='reason',
            field=models.SmallIntegerField(choices=[(1, 'Spam | Exists only to promote a service '), (2, 'Abusive | Intended at promoting hatred'), (100, 'Something else')], default=1),
        ),
    ]