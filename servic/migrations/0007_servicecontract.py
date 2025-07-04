# Generated by Django 5.2.1 on 2025-06-17 18:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servic', '0006_servicecategory_service_serviceimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('accepted', 'Aceptado'), ('in_progress', 'En Progreso'), ('completed', 'Completado'), ('cancelled', 'Cancelado'), ('rejected', 'Rechazado')], default='pending', max_length=20)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(help_text='Descripción detallada del trabajo a realizar')),
                ('location', models.CharField(help_text='Ubicación donde se realizará el servicio', max_length=200)),
                ('rejection_reason', models.TextField(blank=True, help_text='Motivo del rechazo si aplica', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_rating', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('client_review', models.TextField(blank=True, null=True)),
                ('provider_rating', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('provider_review', models.TextField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_contracts', to=settings.AUTH_USER_MODEL)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provider_contracts', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='servic.service')),
            ],
            options={
                'verbose_name': 'Contrato de Servicio',
                'verbose_name_plural': 'Contratos de Servicios',
                'ordering': ['-created_at'],
            },
        ),
    ]
