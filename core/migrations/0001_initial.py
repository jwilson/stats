# Generated by Django 3.2.5 on 2021-08-02 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Armor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the armour', max_length=255)),
                ('kind', models.CharField(choices=[('0', 'EMPTY'), ('1', 'HEAD'), ('2', 'SHOULDERS'), ('3', 'CHEST'), ('4', 'WRISTS'), ('5', 'PANTS'), ('6', 'GLOVES'), ('7', 'WAIST'), ('8', 'BOOTS')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the weapon', max_length=255)),
                ('kind', models.CharField(choices=[('0', 'EMPTY'), ('1', 'ONE HAND DAGGER'), ('2', 'ONE HAND MACE'), ('3', 'ONE HAND PISTOL'), ('4', 'ONE HAND SPEAR'), ('5', 'ONE HAND SWORD'), ('6', 'TWO HAND AXE'), ('7', 'TWO HAND BOW'), ('8', 'TWO HAND CROSSBOW'), ('9', 'TWO HAND SHOOTING'), ('10', 'TWO HAND SPEAR'), ('11', 'TWO HAND STAFF'), ('12', 'TWO HAND SWORD'), ('13', 'ITEM'), ('14', 'SHIELD'), ('15', 'UNARMED')], max_length=255)),
            ],
        ),
    ]
