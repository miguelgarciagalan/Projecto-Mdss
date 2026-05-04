from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iniciada', models.DateTimeField(auto_now_add=True)),
                ('historial_pydantic', models.TextField(default='[]')),
            ],
            options={'verbose_name_plural': 'Conversaciones'},
        ),
        migrations.CreateModel(
            name='MensajeConversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes', to='agente.conversacion')),
                ('rol', models.CharField(choices=[('user', 'Usuario'), ('agent', 'Agente')], max_length=10)),
                ('contenido', models.TextField()),
                ('tools_usadas', models.TextField(blank=True, default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['timestamp']},
        ),
    ]
