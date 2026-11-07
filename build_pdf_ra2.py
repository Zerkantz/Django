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
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_FILENAME = "Reporte_RA2_Django_React_JWT_SOAP.pdf"
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
            self.drawString(36, 762, "RA2: Django + React con Autenticacion y APIs (Unidades 2 y 3)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 755, 576, 755)

        page_text = f"Pagina {self._pageNumber} de {page_count}"
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
    success_color = colors.HexColor("#16a34a")
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
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=accent_color,
        spaceBefore=8,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        spaceAfter=6,
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold',
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
    )

    caption_style = ParagraphStyle(
        'Caption_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748b"),
        alignment=1,
        spaceBefore=4,
        spaceAfter=8,
    )

    story = []

    # Portada / Encabezado
    story.append(Paragraph("Resultado de Aprendizaje (RA2 y RA3)", title_style))
    story.append(Paragraph("Desarrollo Full Stack: Django REST Framework + ReactJS + JWT + API de Terceros + SOAP", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=2, spaceAfter=8))

    # Ficha técnica
    meta_data = [
        [Paragraph("<b>Estudiante:</b>", body_style), Paragraph("Ricardo (Zerkantz)", body_style),
         Paragraph("<b>Fecha:</b>", body_style), Paragraph("Noviembre 2026", body_style)],
        [Paragraph("<b>Repositorio GitHub:</b>", body_style),
         Paragraph('<a href="https://github.com/Zerkantz/Django" color="#0284c7"><u>https://github.com/Zerkantz/Django</u></a>', body_style),
         Paragraph("<b>Stack Frontend:</b>", body_style), Paragraph("React 18 + Vite + Semantic UI + SASS", body_style)],
        [Paragraph("<b>Stack Backend:</b>", body_style), Paragraph("Django 5.2 + DRF + SimpleJWT + Zeep", body_style),
         Paragraph("<b>Estado de Pruebas:</b>", body_style), Paragraph("18/18 pruebas superadas (100% OK)", body_style)],
    ]

    meta_table = Table(meta_data, colWidths=[110, 190, 95, 145])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Resumen Ejecutivo
    story.append(Paragraph("1. Resumen de la Solucion Implementada", h1_style))
    resumen_text = (
        "En este entregable integrador de las Unidades 2 y 3, se unifico el backend robusto de Django REST Framework "
        "con una moderna aplicacion Frontend construida en <b>ReactJS con Vite</b>, siguiendo y enriqueciendo "
        "las directrices del manual <i>Desarrollo Full Stack con Django y ReactJS</i>.<br/><br/>"
        "La solucion cubre tres dimensiones fundamentales del desarrollo de software moderno: "
        "<b>(1) Autenticacion y Estado de Sesion</b> mediante tokens JWT (SimpleJWT) y React Context API (<code>AuthContext</code>), "
        "incluyendo Registro publico validado y Login con redireccion automatica; "
        "<b>(2) Integracion Asincrona de APIs REST de Terceros</b> en el Dashboard mediante un widget que consume frases y consejos en tiempo real con <code>fetch()</code>; y "
        "<b>(3) Arquitectura de Web Services Hibrida</b>, ofreciendo Web Services REST propios protegidos (<code>/api/v1/auth/me/</code>) y "
        "un Web Service puente en Django que consume servicios empresariales <b>SOAP / XML</b> publicos utilizando la biblioteca <b>Zeep</b>."
    )
    story.append(Paragraph(resumen_text, body_style))
    story.append(Spacer(1, 6))

    # Componentes Clave
    story.append(Paragraph("2. Arquitectura de Componentes y Funcionalidades", h1_style))

    comp_data = [
        [Paragraph("<b>Componente</b>", body_bold), Paragraph("<b>Tecnologias / Archivos</b>", body_bold), Paragraph("<b>Descripcion y Logica Implementada</b>", body_bold)],
        [
            Paragraph("<b>Frontend SPA</b>", body_style),
            Paragraph("Vite, React 18, React Router v6, Semantic UI", body_style),
            Paragraph("Estructura modular con enrutamiento declarativo (<code>routes.admin</code>, <code>routes.client</code>), layouts desacoplados (<code>AdminLayout</code>, <code>ClientLayout</code>) y estilos SCSS.", body_style)
        ],
        [
            Paragraph("<b>Gestion de Sesion (AuthContext)</b>", body_style),
            Paragraph("<code>src/context/AuthContext.jsx</code><br/><code>src/hooks/useAuth.jsx</code>", body_style),
            Paragraph("Custom hook que mantiene la sesion persistente consultando <code>/api/v1/auth/me/</code> con el token almacenado en <code>localStorage</code>. Provee datos reactivos del usuario y metodo <code>logout()</code>.", body_style)
        ],
        [
            Paragraph("<b>Registro y Login React</b>", body_style),
            Paragraph("Formik + Yup<br/><code>Register.jsx</code> / <code>Login.jsx</code>", body_style),
            Paragraph("Formularios con validacion de esquema. Registro con campo extra <code>telefono</code>, hashing seguro y sanitizacion de datos. Login conectado a <code>/api/v1/auth/token/</code> con redireccion reactiva.", body_style)
        ],
        [
            Paragraph("<b>Widget API de Terceros</b>", body_style),
            Paragraph("API Externa (DummyJSON Quotes)<br/><code>fetch()</code> nativo asincrono", body_style),
            Paragraph("Consumo dinamico de citas/consejos con control de estados de carga, manejo de errores y recarga en vivo (boton <i>Obtener otra frase</i>) incrustado en el Dashboard protegido.", body_style)
        ],
        [
            Paragraph("<b>Consumo SOAP en Django</b>", body_style),
            Paragraph("Biblioteca <code>zeep</code><br/><code>SoapCountryView</code> en <code>users/views.py</code>", body_style),
            Paragraph("Endpoint REST <code>/api/v1/soap/country/</code> que instancia un cliente SOAP sobre el WSDL de <code>CountryInfoService</code>, ejecuta la operacion <code>FullCountryInfo</code> y retorna un JSON estructurado.", body_style)
        ]
    ]

    comp_table = Table(comp_data, colWidths=[120, 150, 270])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 10))

    # Seccion Evidencias
    story.append(PageBreak())
    story.append(Paragraph("3. Evidencias de Ejecucion y Pruebas del Sistema", h1_style))
    story.append(Paragraph(
        "A continuacion se presentan las capturas requeridas por la rubrica demostrando el funcionamiento integral "
        "del frontend, backend, autenticacion por token JWT, API de terceros y Web Service SOAP.",
        body_style
    ))
    story.append(Spacer(1, 6))

    def add_evidence(title, desc, img_rel_path, width=520, height=270):
        img_full_path = os.path.join(EVIDENCIAS_DIR, img_rel_path)
        item = []
        item.append(Paragraph(f"<b>{title}</b>", h2_style))
        item.append(Paragraph(desc, body_style))
        if os.path.exists(img_full_path):
            img = Image(img_full_path, width=width, height=height)
            item.append(img)
            item.append(Paragraph(f"Figura: {title} ({img_rel_path})", caption_style))
        else:
            item.append(Paragraph(f"[ERROR: Imagen no encontrada en {img_full_path}]", code_style))
        item.append(Spacer(1, 8))
        return KeepTogether(item)

    # 1. Registro
    story.append(add_evidence(
        "Evidencia 1: Pantalla de Registro de Nuevos Usuarios en React",
        "Formulario de registro construido con Formik y Yup, integrado al backend mediante el endpoint "
        "<code>POST /api/v1/auth/register/</code>. Se observa la captura del campo personalizado <b>telefono</b>, "
        "la confirmacion de contrasena y la notificacion toast de exito.",
        "ra2_01_registro_react.png",
        width=520,
        height=270
    ))

    # 2. Login y Token JWT en Consola
    story.append(PageBreak())
    story.append(add_evidence(
        "Evidencia 2: Login en React con Token JWT en Consola de DevTools",
        "Peticion de autenticacion exitosa conectada a <code>POST /api/v1/auth/token/</code>. La consola de desarrollo "
        "muestra el token JWT emitido por Django (access y refresh tokens) antes de redirigir al Dashboard protegido.",
        "ra2_02_login_react_consola.png",
        width=520,
        height=270
    ))

    # 3. Dashboard Protegido con AuthContext
    story.append(add_evidence(
        "Evidencia 3: Dashboard Protegido con Datos de Usuario via AuthContext",
        "Panel de administracion protegido que valida la sesion mediante el custom hook <code>useAuth()</code>. "
        "Al recargar o navegar, el contexto consulta <code>/api/v1/auth/me/</code> con el token Bearer persistido en "
        "<code>localStorage</code>, renderizando el email (admin@tiendaonline.local), rol y numero telefonico.",
        "ra2_03_dashboard_protegido.png",
        width=520,
        height=270
    ))

    # 4. Widget de API de Terceros
    story.append(PageBreak())
    story.append(add_evidence(
        "Evidencia 4: Widget de API Externa de Terceros en el Dashboard",
        "Integracion asincrona en el frontend mediante <code>fetch()</code> contra una API REST publica "
        "(DummyJSON Quotes). Muestra la cita inspiracional obtenida, su autor y permite refrescarla en vivo.",
        "ra2_04_widget_api_terceros.png",
        width=520,
        height=270
    ))

    # 5. Consumo SOAP
    story.append(add_evidence(
        "Evidencia 5: Consumo de Servicio Web SOAP Publico con Zeep",
        "Consulta directa en navegador al endpoint propio <code>GET /api/v1/soap/country/?code=MX</code>. "
        "Django actua como cliente SOAP ante <i>CountryInfoService</i> consumiendo su WSDL con la libreria <code>zeep</code> "
        "y devolviendo la respuesta XML transformada en un JSON estructurado con nombre, capital, moneda y telefono de codigo de pais.",
        "ra2_05_consumo_soap.png",
        width=520,
        height=270
    ))

    # Seccion 4: Comandos de Instalacion y Reproducibilidad
    story.append(PageBreak())
    story.append(Paragraph("4. Instrucciones de Instalacion y Ejecucion Local", h1_style))
    story.append(Paragraph(
        "Para desplegar y verificar el sistema completo de forma local, seguir los pasos descritos a continuacion:",
        body_style
    ))

    instructions_html = (
        "<b>1. Clonar el Repositorio:</b><br/>"
        "<code>git clone https://github.com/Zerkantz/Django.git</code><br/>"
        "<code>cd Django</code><br/><br/>"
        "<b>2. Configurar y Ejecutar el Backend (Django):</b><br/>"
        "<code>python -m venv venv</code><br/>"
        "<code>.\\venv\\Scripts\\activate  # En Windows</code><br/>"
        "<code>pip install -r requirements.txt</code><br/>"
        "<code>python manage.py migrate</code><br/>"
        "<code>python manage.py runserver</code><br/>"
        "<i>El backend quedara escuchando en http://127.0.0.1:8000/</i><br/><br/>"
        "<b>3. Configurar y Ejecutar el Frontend (React + Vite):</b><br/>"
        "<code>cd frontend</code><br/>"
        "<code>npm install</code><br/>"
        "<code>npm run dev</code><br/>"
        "<i>El frontend estara disponible en http://127.0.0.1:5173/</i><br/><br/>"
        "<b>4. Ejecutar la Bateria de Pruebas Automatizadas:</b><br/>"
        "<code>python manage.py test users</code><br/>"
        "<i>Garantiza que los 18 casos de prueba (seguridad, JWT, CRUD, SOAP y registro) se ejecuten con 100% de aprobacion.</i>"
    )
    story.append(Paragraph(instructions_html, body_style))
    story.append(Spacer(1, 10))

    # Conclusion
    story.append(Paragraph("5. Conclusiones y Cumplimiento de la Rubrica", h1_style))
    conclusion_text = (
        "Se cumplio a cabalidad con todos los criterios de evaluacion definidos para el <b>Resultado de Aprendizaje 2 y 3</b>:<br/>"
        "- <b>Frontend React Vite:</b> Estructurado con layouts desacoplados, rutas protegidas, Formik, Yup y estilos Semantic UI/SASS.<br/>"
        "- <b>Seguridad y Persistencia JWT:</b> Integracion con SimpleJWT a traves de <code>AuthContext</code> y almacenamiento local validado.<br/>"
        "- <b>Consumo de APIs de Terceros:</b> Widget responsivo integrado en el Dashboard con peticiones asincronas <code>fetch()</code>.<br/>"
        "- <b>Web Services REST y SOAP:</b> Endpoints protegidos REST (<code>/api/v1/auth/me/</code>) y consumo SOAP empresarial con <code>zeep</code>.<br/>"
        "- <b>Calidad de Codigo y Documentacion:</b> Cobertura de tests unitarios/integrales (18/18 OK), documentacion exhaustiva en README.md y sincronizacion con el repositorio oficial."
    )
    story.append(Paragraph(conclusion_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] PDF generado con exito: {PDF_FILENAME}")

if __name__ == "__main__":
    build_pdf()
