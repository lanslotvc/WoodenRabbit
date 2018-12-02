# Generated by Django 2.1 on 2018-09-29 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amber', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbound',
            name='baseprice',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='单价'),
        ),
        migrations.AlterField(
            model_name='inbound',
            name='saleprice',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='售价'),
        ),
        migrations.AlterField(
            model_name='inbound',
            name='type',
            field=models.IntegerField(choices=[(0, '成品'), (1, '原石'), (2, '裸链'), (3, 'K金配件'), (4, '客供制作'), (5, '手工配件'), (6, '配石'), (7, '配件'), (8, '其他配件'), (9, '珍珠'), (10, '古董'), (999, '其他')], default=0, verbose_name='库存类型'),
        ),
        migrations.AlterField(
            model_name='inbound',
            name='weight',
            field=models.FloatField(default=0.0, verbose_name='重量'),
        ),
    ]
