# Tienda Online - Django REST Framework + JWT + Swagger

Proyecto backend desarrollado con **Django 5.2**, **Django REST Framework (DRF)**, autenticación desacoplada **JWT (SimpleJWT)**, documentación interactiva **Swagger OpenAPI (drf-yasg)** y base de datos relacional **MySQL**.

> **Práctica académica:** Basada en el manual *"Desarrollo Full Stack con Django y ReactJS"* (páginas 5 a 12), adaptada con temática propia (**Tienda Online**) y corrigiendo fallas críticas de seguridad presentes en el material didáctico original.

---

## 📌 Características y Adaptaciones Realizadas

1. **Temática Personalizada (Tienda Online):**
   - El proyecto adopta la temática de tienda/comercio electrónico en lugar del nombre genérico `restaurante`.
   - Se refleja en la configuración del proyecto, en el backend y en el título del esquema interactivo de Swagger (`Tienda Online API v1`).

2. **Modelo de Usuario Personalizado (`users.User`):**
   - Hereda de `AbstractUser` de Django.
   - Autenticación con correo electrónico: `USERNAME_FIELD = 'email'`.
   - **Campo extra propio:** Se incorporó el atributo `telefono` (`models.CharField(max_length=20, blank=True, null=True)`).
   - Configurado en el panel **Admin de Django**, en el serializador `UserSerializer` y en la especificación OpenAPI de Swagger.

3. **Configuración de Tiempo de Vida del Token (SimpleJWT):**
   - `ACCESS_TOKEN_LIFETIME = timedelta(hours=2)` (2 horas de vigencia para el token de acceso).
   - `REFRESH_TOKEN_LIFETIME = timedelta(days=7)` (7 días para el token de refresco).
   - Tipo de cabecera: `Authorization: Bearer <access_token>`.

4. **Catálogo de Productos y Categorías (Unidad 1):**
   - Mantenimiento completo de las aplicaciones previas (`CategoryViewSet`, `ProductViewSet`, cálculo de precio final).

---

## 🛡️ Auditoría y Corrección de Fallas de Seguridad

| # | Falla en el Manual Original | Riesgo / Vulnerabilidad | Corrección Implementada |
|---|---|---|---|
| **1** | **Exposición del hash de contraseña** en `UserSerializer` | Al no tener `write_only=True`, cualquier petición `GET` (`/users/`, `/users/{id}/`, `/auth/me/`) exponía los hashes PBKDF2 en texto plano. | Se configuró `extra_kwargs = {'password': {'write_only': True}}`. El hash **nunca** aparece en las respuestas de la API. |
| **2** | **Sobrescritura involuntaria de contraseña en `partial_update`** | El código del manual ejecutaba `else: request.data['password'] = request.user.password`. Si un admin editaba el perfil de un usuario sin enviar contraseña, le transfería su propia contraseña de administrador al usuario editado. | Se eliminó dicha asignación. En `partial_update` y `update`, la contraseña **solo** se modifica si viene explícitamente en el payload con un nuevo valor. |

---

## 🚀 Endpoints Principales de la API

La API se encuentra versionada bajo el prefijo `/api/v1/`:

### Autenticación y Perfil
- `POST /api/v1/auth/token/`: Obtención del par de tokens (Access y Refresh) enviando `email` y `password`.
- `POST /api/v1/auth/token/refresh/`: Renovación del Access Token enviando el Refresh Token.
- `GET /api/v1/auth/me/`: Consulta de datos personales del usuario autenticado (requiere `Authorization: Bearer <token>`).

### Gestión de Usuarios (CRUD Administrativo)
- `GET /api/v1/users/`: Listado de usuarios (requiere `is_staff=True`).
- `POST /api/v1/users/`: Creación de un nuevo usuario.
- `GET /api/v1/users/{id}/`: Detalle de usuario.
- `PUT /api/v1/users/{id}/`: Actualización total.
- `PATCH /api/v1/users/{id}/`: Actualización parcial segura (no altera password si no se envía).
- `DELETE /api/v1/users/{id}/`: Eliminación de usuario.

### Catálogo de Tienda (Productos y Categorías)
- `GET`, `POST` `/api/v1/categories/`
- `GET`, `PUT`, `PATCH`, `DELETE` `/api/v1/categories/{id}/`
- `GET`, `POST` `/api/v1/products/`
- `GET`, `PUT`, `PATCH`, `DELETE` `/api/v1/products/{id}/`
- `GET` `/api/v1/products/{id}/precio-final/`: Cálculo de precio final con descuento.

### Documentación de la API
- **Swagger UI:** `http://127.0.0.1:8000/swagger/`
- **ReDoc:** `http://127.0.0.1:8000/redoc/`
- **OpenAPI JSON:** `http://127.0.0.1:8000/swagger/?format=openapi`

---

## 🛠️ Instalación y Puesta en Marcha

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Zerkantz/Django.git
   cd Django
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos (MySQL):**
   Asegúrese de tener MySQL corriendo con la base de datos `django_api` o modifique las credenciales en `tienda_online/settings.py`.

5. **Aplicar migraciones y crear superusuario:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

---

## 🧪 Ejecución de Pruebas Automatizadas

El proyecto incluye una suite de 16 pruebas unitarias e integrales en `users/tests.py` y `products/tests.py`:

```bash
python manage.py test
```

Salida esperada:
```text
Creating test database for alias 'default'...
................
----------------------------------------------------------------------
Ran 16 tests in 5.8s

OK
```

---

## 📄 Documentación y Reporte en PDF

- **Documento PDF oficial de entrega:** [`Reporte_Practica_Django_DRF_JWT.pdf`](Reporte_Practica_Django_DRF_JWT.pdf)
- **Capturas de pantalla de evidencia:** Almacenadas en la carpeta [`docs/evidencias/`](docs/evidencias/)
  - `01_swagger_endpoints.png`: Documentación interactiva Swagger UI.
  - `02_django_admin_users.png`: Panel Admin de Django con el campo extra `telefono`.
  - `03_obtencion_token_jwt.png`: Petición `POST /api/v1/auth/token/` con email.
  - `04_datos_personales_auth_me.png`: Petición `GET /api/v1/auth/me/` con JWT (sin hash).
  - `05_prueba_seguridad_edicion_sin_password.png`: Prueba de seguridad de actualización sin contraseña.
