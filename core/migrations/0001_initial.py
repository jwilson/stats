# Generated by Django 3.2.6 on 2021-08-29 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the overall organization', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The full name of the player.', max_length=255)),
                ('position', models.CharField(choices=[('RB', 'Runningback'), ('QB', 'Quarterback'), ('WR', 'Wide Receiver'), ('FB', 'Fullback'), ('P', 'Punter'), ('TE', 'Tightend'), ('NT', 'Nose Tackle'), ('DB', 'Defensiveback'), ('SS', 'Strong Safety'), ('K', 'Kicker')], help_text="The player's position", max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The long form team name (ex. Seattle Seahawks)', max_length=255)),
                ('abbreviation', models.CharField(help_text='The abbreviation of the team (ex. SEA)', max_length=255)),
                ('nfl_com_link', models.CharField(help_text='The nfl.com team website address.', max_length=255)),
                ('alternate_abbreviation', models.CharField(help_text='The alternate/newer  abbreviation of the team (ex. LAC)', max_length=255)),
                ('conference', models.CharField(choices=[('AFC', 'AFC'), ('NFC', 'NFC')], help_text='The division the team is currently in.', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerSeasonStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempts', models.PositiveIntegerField(default=0)),
                ('attempts_game', models.FloatField(default=0)),
                ('yards', models.IntegerField(default=0)),
                ('average', models.FloatField(default=0)),
                ('yards_game', models.FloatField(default=0)),
                ('touchdowns', models.PositiveIntegerField(default=0)),
                ('longgains', models.IntegerField(default=0)),
                ('longgains_team', models.BooleanField(default=False)),
                ('first_down', models.PositiveIntegerField(default=0)),
                ('first_down_conversion', models.FloatField()),
                ('twenty_plus', models.PositiveIntegerField(default=0)),
                ('forty_plus', models.PositiveIntegerField(default=0)),
                ('fumbles', models.PositiveIntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.team')),
            ],
        ),
    ]
