from io import BytesIO
import os
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .models import Reporte
import datetime

def _register_font():
    """
    Intenta registrar una fuente TTF común para soportar caracteres acentuados.
    Si no encuentra ninguna, retorna 'Helvetica' como fallback.
    """
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        # rutas comunes en Windows (si quieres agregar localmente): C:\\Windows\\Fonts\\DejaVuSans.ttf
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("AppSans", path))
                return "AppSans"
            except Exception:
                continue
    return "Helvetica"

FONT_NAME = _register_font()

def reporte_pdf(request, id):
    """
    Genera y descarga un PDF para el Reporte con id dado usando ReportLab (platypus).
    Reemplaza la vista anterior basada en canvas para manejar ajuste de texto y paginación.
    """
    reporte = get_object_or_404(Reporte, pk=id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    styles = getSampleStyleSheet()
    # Ajustar estilos para usar la fuente registrada
    styles['Title'].fontName = FONT_NAME
    styles['Title'].fontSize = 18
    styles['Title'].leading = 22
    styles['Title'].alignment = TA_CENTER

    styles['Heading2'].fontName = FONT_NAME
    styles['Heading2'].fontSize = 12
    styles['Heading2'].leading = 14

    body_style = ParagraphStyle(
        "Body",
        parent=styles['BodyText'],
        fontName=FONT_NAME,
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
    )

    meta_style = ParagraphStyle(
        "Meta",
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_LEFT,
    )

    story = []

    # Título
    titulo_text = getattr(reporte, "nombre", f"Reporte {reporte.pk}")
    story.append(Paragraph(titulo_text, styles['Title']))
    story.append(Spacer(1, 6))

    # Metadatos
    fecha = getattr(reporte, "fecha", None)
    fecha_str = fecha.strftime("%d/%m/%Y") if fecha else datetime.datetime.now().strftime("%d/%m/%Y")
    meta = f"ID: {reporte.pk} &nbsp;&nbsp; Fecha: {fecha_str}"
    story.append(Paragraph(meta, meta_style))
    story.append(Spacer(1, 12))

    # Cabecera de contenido
    story.append(Paragraph("Contenido", styles['Heading2']))
    story.append(Spacer(1, 6))

    # El contenido puede incluir saltos de línea; Paragraph soporta <br/>
    contenido_raw = getattr(reporte, "contenido", "")
    # Escapar caracteres HTML no deseados no estrictamente necesario si el campo es texto plano.
    contenido_html = "<br/>".join([line for line in str(contenido_raw).splitlines() if line.strip() != ""])
    if not contenido_html:
        contenido_html = "—"

    story.append(Paragraph(contenido_html, body_style))
    story.append(Spacer(1, 12))

    # Tabla con algunos campos adicionales (personalizable)
    table_data = [
        ["Campo", "Valor"],
        ["Nombre", getattr(reporte, "nombre", "—")],
        ["Fecha", fecha_str],
    ]
    table = Table(table_data, colWidths=[50*mm, 100*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
    ]))
    story.append(table)

    # Construir PDF
    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    filename = f"reporte_{reporte.pk}.pdf"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response