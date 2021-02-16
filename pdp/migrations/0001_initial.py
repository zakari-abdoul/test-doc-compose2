# Generated by Django 3.1.5 on 2021-02-15 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pdp_IN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Interval_Time', models.CharField(max_length=25)),
                ('PLMN_Carrier', models.CharField(max_length=100)),
                ('Direction', models.CharField(max_length=40)),
                ('Service', models.CharField(max_length=20)),
                ('Opcode', models.CharField(max_length=100)),
                ('HVA', models.CharField(max_length=40)),
                ('Total_Transactions', models.PositiveIntegerField()),
                ('Failed_Transactions', models.PositiveIntegerField()),
                ('EFF', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pdp_OUT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Interval_Time', models.CharField(max_length=25)),
                ('PLMN_Carrier', models.CharField(max_length=100)),
                ('Direction', models.CharField(max_length=40)),
                ('Service', models.CharField(max_length=20)),
                ('Opcode', models.CharField(max_length=100)),
                ('HVA', models.CharField(max_length=40)),
                ('Total_Transactions', models.PositiveIntegerField()),
                ('Failed_Transactions', models.PositiveIntegerField()),
                ('EFF', models.PositiveIntegerField()),
            ],
        ),
    ]
