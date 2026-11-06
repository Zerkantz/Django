import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_FILENAME = "Reporte_Practica_Django_DRF_JWT.pdf"
EVIDENCIAS_DIR = os.path.join("docs", "evidencias")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748b"))
        if self._pageNumber > 1:
            self.drawString(36, 762, "Práctica: Django + DRF + JWT + Usuario Personalizado | Tienda Online")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 755, 576, 755)

        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(576, 22, page_text)
        self.drawString(36, 22, "Repositorio GitHub: https://github.com/Zerkantz/Django")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 34, 576, 34)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#0f172a")
    accent_color = colors.HexColor("#0284c7")
    text_color = colors.HexColor("#334155")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=accent_color,
        spaceAfter=10,
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=accent_color,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=text_color,
        spaceAfter=5,
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold',
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=3,
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748b"),
        alignment=1,
        spaceBefore=2,
        spaceAfter=6,
    )

    story = []

    # ==========================
    # PÁGINA 1: PORTADA Y ANÁLISIS
    # ==========================
    story.append(Paragraph("Reporte de Práctica: Desarrollo Backend con Django, DRF y JWT", title_style))
    story.append(Paragraph("Proyecto: <b>Tienda Online API</b> | Autor: Ricardo (GitHub: @Zerkantz)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=accent_color, spaceAfter=8))

    meta_data = [
        [
            Paragraph("<b>Estudiante:</b> Ricardo", body_style),
            Paragraph("<b>Repositorio GitHub:</b> <a href='https://github.com/Zerkantz/Django' color='#0284c7'>https://github.com/Zerkantz/Django</a>", body_style),
        ],
        [
            Paragraph("<b>Tema del Proyecto:</b> Tienda Online (Comercio Electrónico)", body_style),
            Paragraph("<b>Tecnologías:</b> Django 5.2, DRF, SimpleJWT, Swagger (drf-yasg), MySQL", body_style),
        ],
        [
            Paragraph("<b>Campo extra en Usuario:</b> <code>telefono</code>", body_style),
            Paragraph("<b>Tiempo de vida Access Token:</b> 2 horas (<code>ACCESS_TOKEN_LIFETIME</code>)", body_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[240, 300])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Objetivo y Adaptaciones Realizadas", h1_style))
    story.append(Paragraph(
        "Se implementó y fortaleció el backend guiado por el manual <i>'Desarrollo Full Stack con Django y ReactJS'</i> (págs. 5 a 12), adaptándolo a una temática personalizada y solventando fallas de seguridad del diseño original. Partiendo del proyecto de la Unidad 1 (Django + MySQL + DRF + Catálogo de Productos), se incorporaron los siguientes cambios:",
        body_style
    ))
    story.append(Paragraph("• <b>Temática y Nombre Propio:</b> Se definió el proyecto como <b>Tienda Online</b> (reemplazando el nombre 'restaurante'), utilizándolo como núcleo del backend y en el encabezado de Swagger OpenAPI.", bullet_style))
    story.append(Paragraph("• <b>Modelo de Usuario Personalizado:</b> Modelo <code>users.User</code> heredando de <code>AbstractUser</code> con <code>USERNAME_FIELD = 'email'</code> para login con correo.", bullet_style))
    story.append(Paragraph("• <b>Campo Extra Personalizado (<code>telefono</code>):</b> Añadido al modelo, reflejado en el panel Admin de Django, en el serializador <code>UserSerializer</code> y en los esquemas OpenAPI de Swagger.", bullet_style))
    story.append(Paragraph("• <b>Tiempo de Vida del Token JWT:</b> Configuración explícita de <code>ACCESS_TOKEN_LIFETIME = timedelta(hours=2)</code> y <code>REFRESH_TOKEN_LIFETIME = timedelta(days=7)</code> en <code>settings.py</code>.", bullet_style))

    story.append(Paragraph("2. Identificación y Corrección de Fallas de Seguridad", h1_style))
    story.append(Paragraph(
        "El código base del manual presentaba dos fallas de seguridad críticas que fueron identificadas y corregidas:",
        body_style
    ))

    vuln_data = [
        [
            Paragraph("<b>Falla en Manual Original</b>", body_bold),
            Paragraph("<b>Impacto / Vulnerabilidad</b>", body_bold),
            Paragraph("<b>Corrección Implementada</b>", body_bold),
        ],
        [
            Paragraph("<b>1. Fuga de Contraseña:</b><br/>El <code>UserSerializer</code> incluía el campo <code>password</code> sin <code>write_only=True</code>.", body_style),
            Paragraph("Toda respuesta GET (incluido <code>/api/v1/auth/me/</code>) exponía el hash PBKDF2 de la contraseña del usuario en texto plano.", body_style),
            Paragraph("Se configuró <code>extra_kwargs = {'password': {'write_only': True}}</code>. La contraseña puede recibirse al crear o actualizar, pero <b>nunca</b> se serializa en respuestas.", body_style),
        ],
        [
            Paragraph("<b>2. Sobrescritura de Contraseña:</b><br/>En <code>partial_update</code> del viewset:<br/><code>else: data['password'] = request.user.password</code>", body_style),
            Paragraph("Al actualizar un usuario sin enviar contraseña, el manual le asignaba la contraseña encriptada del admin peticionario. El usuario perdía su contraseña original.", body_style),
            Paragraph("Se eliminó dicha asignación. En <code>partial_update</code> y <code>update</code> solo se altera la contraseña si viene explícitamente en el payload con un nuevo valor.", body_style),
        ]
    ]

    vuln_table = Table(vuln_data, colWidths=[170, 170, 200])
    vuln_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0f2fe")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(vuln_table)

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 2: SWAGGER Y DJANGO ADMIN
    # ==========================================
    story.append(Paragraph("3. Evidencias Gráficas del Sistema", h1_style))

    story.append(Paragraph("3.1 Documentación Interactiva Swagger (drf-yasg)", h2_style))
    story.append(Paragraph("Esquema OpenAPI interactivo con título <b>'Tienda Online API v1'</b>, exponiendo los endpoints de Usuarios, Autenticación JWT, Categorías y Productos:", body_style))
    img_sw_path = os.path.join(EVIDENCIAS_DIR, "01_swagger_endpoints.png")
    if os.path.exists(img_sw_path):
        story.append(Image(img_sw_path, width=510, height=270))
        story.append(Paragraph("Figura 1: Interfaz Swagger UI en <code>http://127.0.0.1:8000/swagger/</code> con los módulos organizados.", caption_style))

    story.append(Spacer(1, 4))

    story.append(Paragraph("3.2 Panel de Administración de Django con Campo Extra 'Teléfono'", h2_style))
    story.append(Paragraph("Visualización del modelo de usuario en el Django Admin, destacando la columna personalizada <b>'TELÉFONO'</b> y el inicio de sesión con email:", body_style))
    img_adm_path = os.path.join(EVIDENCIAS_DIR, "02_django_admin_users.png")
    if os.path.exists(img_adm_path):
        story.append(Image(img_adm_path, width=510, height=240))
        story.append(Paragraph("Figura 2: Django Admin con el modelo de usuarios personalizado y el campo extra <code>telefono</code>.", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 3: OBTENCIÓN TOKEN Y AUTH/ME
    # ==========================================
    story.append(Paragraph("3.3 Obtención del Token JWT (/api/v1/auth/token/)", h2_style))
    story.append(Paragraph("Inicio de sesión por email y contraseña. Se comprueba la entrega de <code>access</code> (vida útil de 2 horas) y <code>refresh</code> token:", body_style))
    img_tok_path = os.path.join(EVIDENCIAS_DIR, "03_obtencion_token_jwt.png")
    if os.path.exists(img_tok_path):
        story.append(Image(img_tok_path, width=510, height=265))
        story.append(Paragraph("Figura 3: Petición POST a <code>/api/v1/auth/token/</code> con email retornando tokens de autenticación.", caption_style))

    story.append(Spacer(1, 4))

    story.append(Paragraph("3.4 Consulta de Datos Personales (/api/v1/auth/me/)", h2_style))
    story.append(Paragraph("Petición GET autenticada mediante cabecera <code>Authorization: Bearer &lt;token&gt;</code>. Se verifica la presencia del campo extra <code>telefono</code> y la exclusión absoluta del campo <code>password</code>:", body_style))
    img_me_path = os.path.join(EVIDENCIAS_DIR, "04_datos_personales_auth_me.png")
    if os.path.exists(img_me_path):
        story.append(Image(img_me_path, width=510, height=265))
        story.append(Paragraph("Figura 4: Endpoint <code>/api/v1/auth/me/</code> con datos del usuario. Corrección de seguridad verificada (sin hash de password).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 4: PRUEBA DE SEGURIDAD Y TESTS
    # ==========================================
    story.append(Paragraph("3.5 Prueba Crítica de Seguridad: Edición sin Contraseña", h2_style))
    story.append(Paragraph("Demostración experimental de que al editar un usuario sin enviar contraseña (PATCH), se conservan sus datos previos y <b>NO</b> se le asigna la contraseña del administrador:", body_style))
    img_sec_path = os.path.join(EVIDENCIAS_DIR, "05_prueba_seguridad_edicion_sin_password.png")
    if os.path.exists(img_sec_path):
        story.append(Image(img_sec_path, width=510, height=365))
        story.append(Paragraph("Figura 5: PATCH sin contraseña -> Login con contraseña original: 200 OK -> Login con contraseña de admin: 401 Rechazado.", caption_style))

    story.append(Spacer(1, 4))

    story.append(Paragraph("4. Verificación Automatizada con Django Tests", h1_style))
    story.append(Paragraph("Se construyeron 16 pruebas unitarias e integrales (100% aprobadas) para garantizar la calidad del software:", body_style))

    test_data = [
        [Paragraph("<b>Módulo de Pruebas</b>", body_bold), Paragraph("<b>Aspectos Validados</b>", body_bold), Paragraph("<b>Resultado</b>", body_bold)],
        [Paragraph("<code>UserModelTestCase</code>", body_style), Paragraph("Creación con email, teléfono y superusuario con permisos.", body_style), Paragraph("<font color='#16a34a'><b>PASÓ (OK)</b></font>", body_style)],
        [Paragraph("<code>SecurityFixesTestCase</code>", body_style), Paragraph("Validación de no exposición de password y preservación en PATCH.", body_style), Paragraph("<font color='#16a34a'><b>PASÓ (OK)</b></font>", body_style)],
        [Paragraph("<code>JWTAuthenticationTestCase</code>", body_style), Paragraph("Emisión con email, expiración en 7200 s y consumo en <code>/auth/me/</code>.", body_style), Paragraph("<font color='#16a34a'><b>PASÓ (OK)</b></font>", body_style)],
        [Paragraph("<code>CategoryTestCase</code>", body_style), Paragraph("Creación y listado de categorías en la API REST.", body_style), Paragraph("<font color='#16a34a'><b>PASÓ (OK)</b></font>", body_style)],
        [Paragraph("<code>ProductTestCase</code>", body_style), Paragraph("CRUD completo y endpoint de precio final con descuento.", body_style), Paragraph("<font color='#16a34a'><b>PASÓ (OK)</b></font>", body_style)],
    ]
    t_table = Table(test_data, colWidths=[150, 270, 120])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_table)

    story.append(PageBreak())

    # ==========================================
    # PÁGINA 5: CONCLUSIONES Y ENTREGA
    # ==========================================
    story.append(Paragraph("5. Conclusiones y Consideraciones Finales", h1_style))
    story.append(Paragraph(
        "El desarrollo de esta práctica permitió consolidar la implementación de arquitecturas de autenticación desacopladas "
        "con JSON Web Tokens (JWT) en Django REST Framework, integrando un modelo de usuario personalizado basado en correo "
        "electrónico y extendido con atributos propios de la aplicación (<code>telefono</code>).",
        body_style
    ))
    story.append(Paragraph(
        "Un aprendizaje fundamental del ejercicio fue el rigor en la auditoría de seguridad del código fuente: los manuales y "
        "guías de introducción a menudo omiten validaciones estrictas o introducen atajos metodológicos que, de aplicarse en "
        "producción, expondrían credenciales confidenciales o vulnerarían cuentas de usuarios. Corregir estas dos debilidades "
        "(restringir el hash a <code>write_only</code> y preservar la integridad del password en actualizaciones parciales) "
        "eleva el proyecto a estándares profesionales de seguridad en software.",
        body_style
    ))

    story.append(Spacer(1, 10))

    delivery_box_data = [
        [
            Paragraph(
                "<b>DATOS DE ENTREGA Y REPOSITORIO DEL PROYECTO</b><br/><br/>"
                "<b>Enlace Oficial del Repositorio de GitHub:</b><br/>"
                "<a href='https://github.com/Zerkantz/Django' color='#0284c7'><b>https://github.com/Zerkantz/Django</b></a><br/><br/>"
                "<b>Elementos clave verificados en el repositorio:</b><br/>"
                "• <b>.gitignore:</b> Excluye entornos virtuales (<code>venv/</code>, <code>.venv/</code>), bases de datos locales (<code>db.sqlite3</code>), archivos de caché de Python (<code>__pycache__/</code>, <code>*.pyc</code>) y temporales.<br/>"
                "• <b>requirements.txt:</b> Dependencias completas en UTF-8 (Django 5.2, DRF 3.18, djangorestframework-simplejwt, drf-yasg, mysqlclient, reportlab, etc.).<br/>"
                "• <b>users app:</b> Modelo <code>User</code> personalizado, endpoints de autenticación JWT (<code>/api/v1/auth/token/</code>, <code>/api/v1/auth/token/refresh/</code>), endpoint de datos propios (<code>/api/v1/auth/me/</code>) y CRUD administrativo de usuarios.<br/>"
                "• <b>products app:</b> Integración completa del catálogo de la Unidad 1 (Categorías, Productos y Cálculo de Precio Final).<br/>"
                "• <b>Documentación interactiva:</b> Swagger UI disponible en <code>/swagger/</code> y ReDoc en <code>/redoc/</code>.",
                callout_style
            )
        ]
    ]
    delivery_table = Table(delivery_box_data, colWidths=[540])
    delivery_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0fdf4")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#16a34a")),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(delivery_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {PDF_FILENAME}")

if __name__ == "__main__":
    build_pdf()
