import os
from dataclasses import dataclass

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from gestion_usuarios.models import Productor
from gestion_materia_prima.models import LoteMateriaPrima, ResultadoAnalisis
from gestion_produccion.models import LoteProduccion, ProductoFinal


@dataclass
class CooperativaDeps:
    pass


class RespuestaCooperativa(BaseModel):
    mensaje: str = Field(description="Respuesta en lenguaje natural al usuario")


cooperativa_agent = Agent(
    os.environ.get('AI_MODEL', 'openai:gpt-4o-mini'),
    deps_type=CooperativaDeps,
    output_type=RespuestaCooperativa,
    instructions="""
Eres un asistente especializado en la gestión de la Cooperativa Olivícola.

El sistema gestiona:
- Productores: agricultores que entregan aceituna
- Lotes de materia prima: aceituna recibida (estados: INGRESADO → ANALISIS → ANALIZADO → ASIGNADO)
- Resultados de análisis: análisis realizados a cada lote
- Lotes de producción: agrupan lotes de MP para producir aceite (estados: ARMADO → FINALIZADO)
- Productos finales: aceite u oliva de mesa obtenidos de un lote de producción

Reglas de negocio:
- Un lote de MP solo puede asignarse a producción si está en estado ANALIZADO
- Un lote de producción solo puede finalizarse si tiene productos finales registrados
- Los estados siguen una secuencia estricta y no son reversibles

Instrucciones:
- Responde siempre en español
- No inventes datos: usa las herramientas para consultar información real
- Si una acción no es posible, explica claramente el motivo
- Usa el código del lote exactamente como lo proporciona el usuario
""",
)


@cooperativa_agent.tool
def listar_lotes_materia_prima(
    ctx: RunContext[CooperativaDeps],
    estado: str | None = None,
) -> list[dict]:
    """
    Lista los lotes de materia prima del sistema.
    Filtra opcionalmente por estado: INGRESADO, ANALISIS, ANALIZADO o ASIGNADO.

    Args:
        estado: Estado por el que filtrar. Si no se indica, devuelve todos.
    """
    qs = LoteMateriaPrima.objects.select_related('productor').order_by('-fecha_arribo')
    if estado:
        qs = qs.filter(estado=estado.upper())
    return [
        {
            'id': lote.id,
            'codigo': lote.codigo,
            'productor': f'{lote.productor.nombre} {lote.productor.apellidos}',
            'fecha_cosecha': str(lote.fecha_cosecha),
            'peso_neto_kg': lote.peso_neto,
            'estado': lote.get_estado_display(),
        }
        for lote in qs[:20]
    ]


@cooperativa_agent.tool
def obtener_detalle_lote_materia_prima(
    ctx: RunContext[CooperativaDeps],
    codigo: str,
) -> dict | None:
    """
    Obtiene el detalle completo de un lote de materia prima por su código,
    incluyendo productor, pesos y resultados de análisis asociados.

    Args:
        codigo: Código único del lote de materia prima.
    """
    try:
        lote = (
            LoteMateriaPrima.objects
            .select_related('productor')
            .prefetch_related('analisis')
            .get(codigo=codigo)
        )
    except LoteMateriaPrima.DoesNotExist:
        return None

    return {
        'id': lote.id,
        'codigo': lote.codigo,
        'productor': f'{lote.productor.nombre} {lote.productor.apellidos} (NIF: {lote.productor.nif})',
        'fecha_cosecha': str(lote.fecha_cosecha),
        'fecha_arribo': str(lote.fecha_arribo),
        'peso_bruto_kg': lote.peso_bruto,
        'peso_tara_kg': lote.peso_tara,
        'peso_neto_kg': lote.peso_neto,
        'estado': lote.get_estado_display(),
        'analisis': [
            {'tipo': a.tipo_analisis, 'fecha': str(a.fecha_hora)}
            for a in lote.analisis.all()
        ],
    }


@cooperativa_agent.tool
def listar_lotes_produccion(
    ctx: RunContext[CooperativaDeps],
    estado: str | None = None,
) -> list[dict]:
    """
    Lista los lotes de producción del sistema.
    Filtra opcionalmente por estado: ARMADO o FINALIZADO.

    Args:
        estado: Estado por el que filtrar. Si no se indica, devuelve todos.
    """
    qs = LoteProduccion.objects.prefetch_related('lotes_materia_prima', 'productos_finales').order_by('-fecha_creacion')
    if estado:
        qs = qs.filter(estado=estado.upper())
    return [
        {
            'id': lote.id,
            'codigo_seguimiento': lote.codigo_seguimiento,
            'fecha_creacion': str(lote.fecha_creacion),
            'estado': lote.get_estado_display(),
            'num_lotes_mp': lote.lotes_materia_prima.count(),
            'num_productos_finales': lote.productos_finales.count(),
            'peso_total_neto_kg': lote.peso_total_neto,
        }
        for lote in qs[:20]
    ]


@cooperativa_agent.tool
def validar_lote_para_produccion(
    ctx: RunContext[CooperativaDeps],
    codigo: str,
) -> dict:
    """
    Valida si un lote de materia prima puede ser asignado a un lote de producción.
    Comprueba que exista, esté en estado ANALIZADO y tenga al menos un análisis registrado.

    Args:
        codigo: Código del lote de materia prima a validar.
    """
    try:
        lote = LoteMateriaPrima.objects.prefetch_related('analisis').get(codigo=codigo)
    except LoteMateriaPrima.DoesNotExist:
        return {'valido': False, 'motivo': f'No existe ningún lote con código {codigo}.'}

    if lote.estado == 'ASIGNADO':
        return {'valido': False, 'motivo': 'El lote ya está asignado a un lote de producción.'}

    if lote.estado != 'ANALIZADO':
        return {
            'valido': False,
            'motivo': f'El lote está en estado "{lote.get_estado_display()}". Debe estar en estado ANALIZADO.',
        }

    if not lote.analisis.exists():
        return {'valido': False, 'motivo': 'El lote no tiene ningún resultado de análisis registrado.'}

    return {'valido': True, 'motivo': 'El lote cumple todos los requisitos para ser asignado a producción.'}


@cooperativa_agent.tool
def crear_lote_produccion(
    ctx: RunContext[CooperativaDeps],
    codigos_lotes_mp: list[str],
) -> dict:
    """
    Crea un nuevo lote de producción asignando los lotes de materia prima indicados.
    Los lotes deben estar en estado ANALIZADO. Al asignarlos pasan a estado ASIGNADO.

    Args:
        codigos_lotes_mp: Lista de códigos de lotes de materia prima a incluir.
    """
    lotes = []
    errores = []

    for codigo in codigos_lotes_mp:
        try:
            lote = LoteMateriaPrima.objects.get(codigo=codigo)
            if lote.estado != 'ANALIZADO':
                errores.append(f'{codigo}: estado actual es "{lote.get_estado_display()}", se requiere ANALIZADO.')
            else:
                lotes.append(lote)
        except LoteMateriaPrima.DoesNotExist:
            errores.append(f'{codigo}: lote no encontrado.')

    if errores:
        return {'creado': False, 'errores': errores}

    lote_produccion = LoteProduccion.objects.create(estado='ARMADO')
    lote_produccion.lotes_materia_prima.set(lotes)
    LoteMateriaPrima.objects.filter(id__in=[l.id for l in lotes]).update(estado='ASIGNADO')

    return {
        'creado': True,
        'codigo_seguimiento': lote_produccion.codigo_seguimiento,
        'lotes_asignados': codigos_lotes_mp,
        'estado': 'ARMADO',
    }


@cooperativa_agent.tool
def resumen_sistema(ctx: RunContext[CooperativaDeps]) -> dict:
    """
    Devuelve un resumen general del estado del sistema: totales de productores,
    lotes de materia prima por estado, lotes de producción y productos finales.
    """
    return {
        'productores': Productor.objects.count(),
        'lotes_materia_prima': {
            'total': LoteMateriaPrima.objects.count(),
            'ingresados': LoteMateriaPrima.objects.filter(estado='INGRESADO').count(),
            'en_analisis': LoteMateriaPrima.objects.filter(estado='ANALISIS').count(),
            'analizados': LoteMateriaPrima.objects.filter(estado='ANALIZADO').count(),
            'asignados': LoteMateriaPrima.objects.filter(estado='ASIGNADO').count(),
        },
        'lotes_produccion': {
            'total': LoteProduccion.objects.count(),
            'en_armado': LoteProduccion.objects.filter(estado='ARMADO').count(),
            'finalizados': LoteProduccion.objects.filter(estado='FINALIZADO').count(),
        },
        'productos_finales': ProductoFinal.objects.count(),
    }


@cooperativa_agent.tool
def generar_informe_lote_produccion(
    ctx: RunContext[CooperativaDeps],
    codigo_seguimiento: str,
) -> str:
    """
    Genera un informe de texto completo de un lote de producción:
    lotes de materia prima asociados, pesos, análisis y productos finales.

    Args:
        codigo_seguimiento: Código de seguimiento del lote de producción.
    """
    try:
        lote = LoteProduccion.objects.prefetch_related(
            'lotes_materia_prima__productor',
            'lotes_materia_prima__analisis',
            'productos_finales',
        ).get(codigo_seguimiento=codigo_seguimiento)
    except LoteProduccion.DoesNotExist:
        return f'No existe ningún lote de producción con código {codigo_seguimiento}.'

    lineas = [
        f'INFORME — LOTE DE PRODUCCIÓN {lote.codigo_seguimiento}',
        f'Estado: {lote.get_estado_display()}',
        f'Fecha de creación: {lote.fecha_creacion.strftime("%d/%m/%Y %H:%M")}',
        f'Peso total neto: {lote.peso_total_neto:.1f} kg',
        '',
        f'LOTES DE MATERIA PRIMA ({lote.lotes_materia_prima.count()}):',
    ]
    for mp in lote.lotes_materia_prima.all():
        lineas.append(
            f'  · {mp.codigo}  |  {mp.productor.nombre} {mp.productor.apellidos}'
            f'  |  {mp.peso_neto} kg  |  {mp.get_estado_display()}'
        )
        for a in mp.analisis.all():
            lineas.append(f'      Análisis: {a.tipo_analisis} ({a.fecha_hora.strftime("%d/%m/%Y")})')

    lineas += ['', f'PRODUCTOS FINALES ({lote.productos_finales.count()}):']
    for pf in lote.productos_finales.all():
        lineas.append(
            f'  · {pf.nombre}  |  {pf.get_tipo_display()}'
            f'  |  {pf.cantidad} {pf.get_unidad_display()}'
        )

    return '\n'.join(lineas)
