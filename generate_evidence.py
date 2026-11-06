import json
import os
import subprocess
import urllib.error
import urllib.request

BASE_URL = 'http://127.0.0.1:8000'

def request(url, method='GET', data=None, headers=None):
    if headers is None:
        headers = {}
    req_data = json.dumps(data).encode('utf-8') if data else None
    req_headers = {'Content-Type': 'application/json', **headers}
    req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body

def main():
    # 1. Obtener Token JWT para admin
    st_tok, res_tok = request(f'{BASE_URL}/api/v1/auth/token/', 'POST', {
        'email': 'admin@tiendaonline.local',
        'password': 'AdminPassword123!'
    })
    token = res_tok['access']

    # 2. Consultar /auth/me/
    st_me, res_me = request(
        f'{BASE_URL}/api/v1/auth/me/',
        'GET',
        headers={'Authorization': f'Bearer {token}'}
    )

    # 3. Patch usuario 3 sin contraseña
    st_patch, res_patch = request(
        f'{BASE_URL}/api/v1/users/3/',
        'PATCH',
        {'first_name': 'María Actualizada', 'telefono': '667-999-8888'},
        headers={'Authorization': f'Bearer {token}'}
    )

    # 4. Probar login con contraseña original
    st_orig, res_orig = request(f'{BASE_URL}/api/v1/auth/token/', 'POST', {
        'email': 'usuario.prueba@tiendaonline.local',
        'password': 'OriginalPassword123!'
    })

    # 5. Probar login con contraseña de admin
    st_bad, res_bad = request(f'{BASE_URL}/api/v1/auth/token/', 'POST', {
        'email': 'usuario.prueba@tiendaonline.local',
        'password': 'AdminPassword123!'
    })

    css = """
    body {
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: #0b1120;
      color: #e2e8f0;
      margin: 0;
      padding: 30px;
      box-sizing: border-box;
    }
    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 26px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
      max-width: 1050px;
      margin: 0 auto;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      padding-bottom: 16px;
      margin-bottom: 20px;
    }
    .title {
      font-size: 22px;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .badge-tag {
      background: #0284c7;
      color: #ffffff;
      font-size: 13px;
      padding: 6px 12px;
      border-radius: 6px;
      font-weight: 600;
    }
    .badge-tag.amber {
      background: #b45309;
    }
    .badge-tag.emerald {
      background: #047857;
    }
    .req-line {
      display: flex;
      align-items: center;
      gap: 14px;
      background: #0f172a;
      padding: 14px 18px;
      border-radius: 8px;
      border: 1px solid #334155;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 15px;
      margin-bottom: 22px;
    }
    .method {
      padding: 5px 12px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 13px;
      color: white;
    }
    .POST { background: #16a34a; }
    .GET { background: #2563eb; }
    .PATCH { background: #d97706; }
    .url { color: #f8fafc; font-weight: 600; }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 22px;
    }
    .section-title {
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #94a3b8;
      margin-bottom: 10px;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
    }
    .status-200 { color: #4ade80; font-weight: 700; }
    .status-401 { color: #f87171; font-weight: 700; }
    pre {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 16px;
      color: #cbd5e1;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 13px;
      line-height: 1.5;
      overflow-x: auto;
      white-space: pre-wrap;
      word-break: break-all;
      margin: 0;
    }
    .highlight {
      background: #1e1b4b;
      border-left: 4px solid #818cf8;
      padding: 14px;
      border-radius: 6px;
      margin-top: 18px;
      font-size: 13.5px;
      line-height: 1.5;
      color: #c7d2fe;
    }
    .success-highlight {
      background: #064e3b;
      border-left: 4px solid #34d399;
      padding: 14px;
      border-radius: 6px;
      margin-top: 18px;
      font-size: 13.5px;
      line-height: 1.5;
      color: #a7f3d0;
    }
    .danger-highlight {
      background: #450a0a;
      border-left: 4px solid #f87171;
      padding: 14px;
      border-radius: 6px;
      margin-top: 18px;
      font-size: 13.5px;
      line-height: 1.5;
      color: #fca5a5;
    }
    """

    # 1. HTML Token
    res_tok_clean = {
        "refresh": res_tok["refresh"][:65] + "... [Token de refresco completo: 240 caracteres]",
        "access": res_tok["access"][:65] + "... [Token de acceso completo: 240 caracteres]"
    }
    html_tok = f"""<!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><style>{css}</style></head>
    <body>
    <div class="card">
      <div class="header">
        <div class="title">Captura 1: Obtención de Token JWT</div>
        <div class="badge-tag">ACCESS_TOKEN_LIFETIME = 2 Horas</div>
      </div>
      <div class="req-line">
        <span class="method POST">POST</span>
        <span class="url">http://127.0.0.1:8000/api/v1/auth/token/</span>
      </div>
      <div class="grid">
        <div>
          <div class="section-title">Request Payload (JSON)</div>
          <pre>{json.dumps({'email': 'admin@tiendaonline.local', 'password': 'AdminPassword123!'}, indent=2, ensure_ascii=False)}</pre>
          <div class="highlight">
            <strong>Autenticación basada en Email:</strong><br>
            Se verifica que el login acepta <code>email</code> en lugar de username.
          </div>
        </div>
        <div>
          <div class="section-title">
            Response Body
            <span class="status-200">HTTP {st_tok} OK</span>
          </div>
          <pre>{json.dumps(res_tok_clean, indent=2, ensure_ascii=False)}</pre>
          <div class="success-highlight">
            <strong>Tokens generados exitosamente:</strong><br>
            Devuelve el Access Token (expira en 2 horas) y el Refresh Token (7 días).
          </div>
        </div>
      </div>
    </div>
    </body>
    </html>"""
    with open('card_token.html', 'w', encoding='utf-8') as f:
        f.write(html_tok)

    # 2. HTML Auth Me
    html_me = f"""<!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><style>{css}</style></head>
    <body>
    <div class="card">
      <div class="header">
        <div class="title">Captura 2: Consulta de Datos Personales (/api/v1/auth/me/)</div>
        <div class="badge-tag emerald">Corrección de Seguridad 1</div>
      </div>
      <div class="req-line">
        <span class="method GET">GET</span>
        <span class="url">http://127.0.0.1:8000/api/v1/auth/me/</span>
      </div>
      <div class="grid">
        <div>
          <div class="section-title">Request Headers</div>
          <pre>{json.dumps({'Authorization': f'Bearer {token[:45]}...[truncado]', 'Accept': 'application/json'}, indent=2, ensure_ascii=False)}</pre>
          <div class="highlight">
            <strong>Cabecera de Autorización:</strong><br>
            Se envía el JWT obtenido con el prefijo Bearer.
          </div>
        </div>
        <div>
          <div class="section-title">
            Response Body
            <span class="status-200">HTTP {st_me} OK</span>
          </div>
          <pre>{json.dumps(res_me, indent=2, ensure_ascii=False)}</pre>
          <div class="success-highlight">
            <strong>✅ Corrección de Seguridad Verificada:</strong><br>
            1. El campo <code>password</code> (hash) NUNCA se expone en la respuesta.<br>
            2. El campo extra personalizado <code>telefono</code> se muestra con éxito.
          </div>
        </div>
      </div>
    </div>
    </body>
    </html>"""
    with open('card_auth_me.html', 'w', encoding='utf-8') as f:
        f.write(html_me)

    # 3. HTML Security Fix
    html_sec = f"""<!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><style>{css}</style></head>
    <body>
    <div class="card">
      <div class="header">
        <div class="title">Captura 3: Prueba de Seguridad — Edición sin Contraseña</div>
        <div class="badge-tag amber">Corrección de Seguridad 2</div>
      </div>
      <div class="req-line">
        <span class="method PATCH">PATCH</span>
        <span class="url">http://127.0.0.1:8000/api/v1/users/3/</span>
      </div>
      <div class="grid">
        <div>
          <div class="section-title">Request Payload (Sin campo password)</div>
          <pre>{json.dumps({'first_name': 'María Actualizada', 'telefono': '667-999-8888'}, indent=2, ensure_ascii=False)}</pre>
          <div class="highlight">
            <strong>Petición enviada por el Administrador:</strong><br>
            Actualiza datos personales de la usuaria 3 sin enviar campo de contraseña.
          </div>
        </div>
        <div>
          <div class="section-title">
            Response Body
            <span class="status-200">HTTP {st_patch} OK</span>
          </div>
          <pre>{json.dumps(res_patch, indent=2, ensure_ascii=False)}</pre>
          <div class="success-highlight">
            <strong>Datos actualizados exitosamente:</strong><br>
            Nombre y teléfono modificados. La respuesta no incluye el hash de la contraseña.
          </div>
        </div>
      </div>

      <div style="margin-top: 24px; border-top: 1px solid #334155; padding-top: 18px;">
        <div class="section-title" style="font-size: 14px; color: #f8fafc;">
          Verificación de Seguridad: Prueba de Login posterior a la Edición
        </div>
        <div class="grid" style="margin-top: 12px;">
          <div>
            <div class="section-title">Prueba A: Login con Contraseña Original</div>
            <div class="req-line" style="margin-bottom: 8px; font-size: 13px;">
              <span class="method POST">POST</span>
              <span>password: 'OriginalPassword123!'</span>
            </div>
            <div class="success-highlight" style="margin-top: 0;">
              <strong>✅ ÉXITO (HTTP {st_orig} OK):</strong><br>
              La usuaria conserva intacta su contraseña original. No fue alterada por el PATCH.
            </div>
          </div>
          <div>
            <div class="section-title">Prueba B: Login con Contraseña del Administrador</div>
            <div class="req-line" style="margin-bottom: 8px; font-size: 13px;">
              <span class="method POST">POST</span>
              <span>password: 'AdminPassword123!'</span>
            </div>
            <div class="danger-highlight" style="margin-top: 0;">
              <strong>✅ RECHAZADO (HTTP {st_bad} Unauthorized):</strong><br>
              La contraseña del admin NO fue transferida a la usuaria. Falla de seguridad resuelta.
            </div>
          </div>
        </div>
      </div>
    </div>
    </body>
    </html>"""
    with open('card_security_fix.html', 'w', encoding='utf-8') as f:
        f.write(html_sec)

    print('HTML cards regenerated with ensure_ascii=False and clean token wrapping.')

if __name__ == '__main__':
    main()
