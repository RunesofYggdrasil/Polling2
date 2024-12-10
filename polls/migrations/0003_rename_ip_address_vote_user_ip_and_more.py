# Generated by Django 5.1.3 on 2024-12-10 02:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_vote_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='ip_address',
            new_name='user_ip',
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='vote_time',
            new_name='voted_at',
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='choice',
            name='meal',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], default='misc', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question'),
        ),
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
    ]
