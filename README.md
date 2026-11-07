# Tienda Online - Full Stack Django REST Framework + ReactJS + SOAP

Proyecto Full Stack integral desarrollado con **Django 5.2**, **Django REST Framework (DRF)**, **ReactJS (Vite)**, autenticación desacoplada **JWT (SimpleJWT)**, consumo de **APIs de Terceros**, integración de **Web Services SOAP (Zeep)**, documentación interactiva **Swagger OpenAPI (drf-yasg)** y base de datos relacional **MySQL**.

> **Resultado de Aprendizaje (RA2 y RA3):** Basado en el manual *"Desarrollo Full Stack con Django y ReactJS"* (páginas 13 a 37) y la integración de Servicios Web de la Unidad 3, adaptado con temática propia (**Tienda Online**) y suite de pruebas automatizadas al 100%.

---

## 📌 Arquitectura y Módulos Implementados

### 1. Backend en Django REST Framework
- **Modelo de Usuario Personalizado (`users.User`):**
  - Autenticación con email: `USERNAME_FIELD = 'email'`.
  - Campo extra personalizado: `telefono` (`models.CharField(max_length=20, blank=True, null=True)`).
  - Configurado en el panel **Admin de Django**, serializadores y documentación Swagger.
- **Autenticación JWT:**
  - `ACCESS_TOKEN_LIFETIME = timedelta(hours=2)`
  - `REFRESH_TOKEN_LIFETIME = timedelta(days=7)`
  - Encabezado: `Authorization: Bearer <token>`
- **Registro Público:** `POST /api/v1/auth/register/` con validación de seguridad (contraseña mínima de 8 caracteres y confirmación).
- **Web Service Propio Protegido:** `GET /api/v1/auth/me/` para consultar la información del usuario autenticado sin exponer hashes.
- **Web Service SOAP Público:** `GET /api/v1/soap/country/?code=<ISO>` que consume el WSDL de `CountryInfoService` mediante la biblioteca `zeep`.
- **CORS Configurado:** `django-cors-headers` habilitado para comunicación fluida con el frontend React.

### 2. Frontend en React (Vite)
- **Tecnologías:** React 18, React Router DOM v6, Semantic UI React, SASS, Formik, Yup, React Toastify.
- **Estructura Modular:**
  - `src/layouts/`: `AdminLayout`, `ClientLayout`, `CommonLayout`.
  - `src/pages/`: `Dashboard`, `Login`, `Register`, `Home`, `Error404`.
  - `src/routes/`: Enrutamiento declarativo para áreas administrativas, públicas y comunes.
- **Gestión de Sesión Reactiva (`AuthContext` & `useAuth`):**
  - Almacenamiento seguro del Access Token en `localStorage`.
  - Sincronización automática de perfil con `GET /api/v1/auth/me/`.
  - Persistencia de sesión al recargar y cierre de sesión centralizado (`logout`).
- **Integración API de Terceros (Unidad 3):**
  - Widget en el Dashboard protegido que consume asincrónicamente mediante `fetch()` una API externa de frases/citas inspiracionales (DummyJSON Quotes).
  - Incluye estados de carga, manejo de fallos y botón interactivo para refrescar datos.

---

## 🛡️ Auditoría y Corrección de Fallas de Seguridad

| # | Falla en el Manual Original | Riesgo / Vulnerabilidad | Corrección Implementada |
|---|---|---|---|
| **1** | **Exposición del hash de contraseña** en `UserSerializer` | Al no tener `write_only=True`, cualquier petición `GET` (`/users/`, `/users/{id}/`, `/auth/me/`) exponía los hashes PBKDF2 en texto plano. | Se configuró `extra_kwargs = {'password': {'write_only': True}}`. El hash **nunca** aparece en las respuestas de la API. |
| **2** | **Sobrescritura involuntaria de contraseña en `partial_update`** | El código del manual ejecutaba `else: request.data['password'] = request.user.password`. Si un admin editaba el perfil de un usuario sin enviar contraseña, le transfería su propia contraseña de administrador al usuario editado. | Se eliminó dicha asignación. En `partial_update` y `update`, la contraseña **solo** se modifica si viene explícitamente en el payload con un nuevo valor. |

---

## 🚀 Endpoints Principales de la API

La API se encuentra versionada bajo el prefijo `/api/v1/`:

### Autenticación y Usuarios
- `POST /api/v1/auth/register/`: Registro público de usuarios (valida contraseñas coincidentes y campo `telefono`).
- `POST /api/v1/auth/token/`: Obtención de JWT (Access y Refresh).
- `POST /api/v1/auth/token/refresh/`: Renovación del Access Token.
- `GET /api/v1/auth/me/`: Datos personales del usuario logueado (`Bearer <token>`).
- `GET`, `POST`, `PUT`, `PATCH`, `DELETE` `/api/v1/users/`: CRUD administrativo protegido (`is_staff=True`).

### Catálogo de Tienda (Productos y Categorías)
- `GET`, `POST`, `PUT`, `PATCH`, `DELETE` `/api/v1/categories/`
- `GET`, `POST`, `PUT`, `PATCH`, `DELETE` `/api/v1/products/`
- `GET` `/api/v1/products/{id}/precio-final/`: Cálculo de precio final con descuento.

### Web Service SOAP
- `GET /api/v1/soap/country/?code=MX`: Consumo en tiempo real del WSDL `CountryInfoService` a través de `zeep`.

### Documentación Interactiva
- **Swagger UI:** `http://127.0.0.1:8000/swagger/`
- **ReDoc:** `http://127.0.0.1:8000/redoc/`

---

## 🛠️ Instalación y Puesta en Marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/Zerkantz/Django.git
cd Django
```

### 2. Backend (Django)
```bash
# Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/macOS

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Iniciar servidor backend
python manage.py runserver
```
> El backend quedará corriendo en `http://127.0.0.1:8000/`.

### 3. Frontend (React + Vite)
```bash
# Entrar al directorio del frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```
> El frontend estará disponible en `http://127.0.0.1:5173/`.

---

## 🧪 Ejecución de Pruebas Automatizadas

El proyecto incluye 18 casos de prueba automatizados para verificar la autenticación, seguridad, endpoints protegidos, registro y servicios SOAP:

```bash
python manage.py test
```

Resultado de las pruebas:
```text
Creating test database for alias 'default'...
..................
----------------------------------------------------------------------
Ran 18 tests in 6.421s

OK
```

---

## 📄 Documentación y Reportes en PDF

- **Reporte Oficial RA2/RA3 (React + JWT + Terceros + SOAP):** [`Reporte_RA2_Django_React_JWT_SOAP.pdf`](Reporte_RA2_Django_React_JWT_SOAP.pdf)
- **Reporte Práctica 4 (Django + DRF + JWT):** [`Reporte_Practica_Django_DRF_JWT.pdf`](Reporte_Practica_Django_DRF_JWT.pdf)
- **Capturas de evidencia disponibles en [`docs/evidencias/`](docs/evidencias/):**
  - `ra2_01_registro_react.png`: Pantalla de Registro en React con campo `telefono`.
  - `ra2_02_login_react_consola.png`: Login en React mostrando el token JWT en la consola DevTools.
  - `ra2_03_dashboard_protegido.png`: Dashboard protegido mostrando usuario vía `AuthContext`.
  - `ra2_04_widget_api_terceros.png`: Widget de API externa de frases inspiracionales.
  - `ra2_05_consumo_soap.png`: Consumo del servicio SOAP de países desde navegador.
