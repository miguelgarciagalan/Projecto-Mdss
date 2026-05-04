import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .agent import cooperativa_agent, CooperativaDeps
from .models import Conversacion, MensajeConversacion


def _extraer_tools(messages) -> list[str]:
    tools = []
    for msg in messages:
        if hasattr(msg, 'parts'):
            for part in msg.parts:
                if hasattr(part, 'tool_name'):
                    tools.append(part.tool_name)
    return list(dict.fromkeys(tools))


def chat(request):
    conv_id = request.session.get('conversacion_id')
    if conv_id:
        try:
            conv = Conversacion.objects.get(id=conv_id)
        except Conversacion.DoesNotExist:
            conv = Conversacion.objects.create()
            request.session['conversacion_id'] = conv.id
    else:
        conv = Conversacion.objects.create()
        request.session['conversacion_id'] = conv.id

    mensajes = conv.mensajes.all()
    return render(request, 'agente/chat.html', {'mensajes': mensajes})


def nueva_conversacion(request):
    conv = Conversacion.objects.create()
    request.session['conversacion_id'] = conv.id
    return redirect('chat')


@require_POST
def enviar_mensaje(request):
    try:
        data = json.loads(request.body)
        texto = data.get('mensaje', '').strip()
        if not texto:
            return JsonResponse({'error': 'Mensaje vacío.'}, status=400)

        conv_id = request.session.get('conversacion_id')
        if not conv_id:
            return JsonResponse({'error': 'No hay conversación activa.'}, status=400)
        conv = Conversacion.objects.get(id=conv_id)

        MensajeConversacion.objects.create(conversacion=conv, rol='user', contenido=texto)

        from pydantic_ai.messages import ModelMessagesTypeAdapter
        history = (
            ModelMessagesTypeAdapter.validate_json(conv.historial_pydantic)
            if conv.historial_pydantic != '[]'
            else []
        )

        result = cooperativa_agent.run_sync(texto, deps=CooperativaDeps(), message_history=history)

        conv.historial_pydantic = ModelMessagesTypeAdapter.dump_json(result.all_messages()).decode()
        conv.save(update_fields=['historial_pydantic'])

        tools = _extraer_tools(result.new_messages())
        MensajeConversacion.objects.create(
            conversacion=conv,
            rol='agent',
            contenido=result.output.mensaje,
            tools_usadas=', '.join(tools),
        )

        return JsonResponse({'respuesta': result.output.mensaje, 'tools_usadas': tools})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
