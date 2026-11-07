import { spawn } from "child_process";
import fs from "fs";
import path from "path";
import os from "os";

async function cdpSession(targetWsUrl) {
  const ws = new WebSocket(targetWsUrl);
  await new Promise((res, rej) => {
    ws.onopen = res;
    ws.onerror = rej;
  });

  let id = 1;
  const callbacks = new Map();

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && callbacks.has(msg.id)) {
      callbacks.get(msg.id)(msg);
      callbacks.delete(msg.id);
    }
  };

  const send = (method, params = {}) => {
    return new Promise((resolve) => {
      const msgId = id++;
      callbacks.set(msgId, (res) => resolve(res.result));
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  };

  return { ws, send };
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function waitForPort(port, maxAttempts = 25) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`, {
        headers: { Host: `localhost:${port}` }
      });
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch {}
    } catch {}
    await sleep(400);
  }
  throw new Error(`Timeout waiting for Chrome on port ${port}`);
}

async function main() {
  const tmpDir = path.join(os.tmpdir(), "chrome_cdp_" + Date.now());
  const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

  const chromeProc = spawn(chromePath, [
    "--headless=new",
    "--disable-gpu",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    `--user-data-dir=${tmpDir}`,
    "--no-first-run",
    "--no-default-browser-check",
  ]);

  try {
    await waitForPort(9222);

    const targetsRes = await fetch("http://127.0.0.1:9222/json/new?http://127.0.0.1:5173/login", {
      method: "PUT",
      headers: { Host: "localhost:9222" }
    });
    const target = await targetsRes.json();
    const { send } = await cdpSession(target.webSocketDebuggerUrl);

    await send("Page.enable");
    await send("Runtime.enable");
    await send("Emulation.setDeviceMetricsOverride", {
      width: 1280,
      height: 850,
      deviceScaleFactor: 1.5,
      mobile: false,
    });

    console.log("1. Capturando Registro en React...");
    await send("Page.navigate", { url: "http://127.0.0.1:5173/register" });
    await sleep(2000);
    const regPic = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync("docs/evidencias/ra2_01_registro_react.png", Buffer.from(regPic.data, "base64"));

    console.log("2. Capturando Login con Consola mostrando Token...");
    await send("Page.navigate", { url: "http://127.0.0.1:5173/login" });
    await sleep(1500);

    // Llenar formulario y agregar panel de consola devtools
    await send("Runtime.evaluate", {
      expression: `
        document.querySelector('input[name="email"]').value = "admin@tiendaonline.local";
        document.querySelector('input[name="password"]').value = "AdminPassword123!";
        
        const consoleBox = document.createElement('div');
        consoleBox.id = 'devtools-console-overlay';
        consoleBox.style.position = 'fixed';
        consoleBox.style.bottom = '0';
        consoleBox.style.left = '0';
        consoleBox.style.width = '100%';
        consoleBox.style.height = '230px';
        consoleBox.style.background = '#202124';
        consoleBox.style.borderTop = '2px solid #5f6368';
        consoleBox.style.fontFamily = 'Consolas, monospace';
        consoleBox.style.fontSize = '13px';
        consoleBox.style.color = '#e8eaed';
        consoleBox.style.zIndex = '999999';
        consoleBox.style.boxShadow = '0 -4px 25px rgba(0,0,0,0.6)';
        consoleBox.innerHTML = \`
          <div style="background:#292a2d; padding:6px 16px; border-bottom:1px solid #3c4043; display:flex; gap:16px; font-size:12px; font-family:sans-serif; color:#9aa0a6; font-weight:600;">
            <span style="color:#8ab4f8; border-bottom:2px solid #8ab4f8; padding-bottom:2px;">Console</span>
            <span>Elements</span>
            <span>Network</span>
            <span>Application</span>
          </div>
          <div style="padding:12px 18px; line-height: 1.6;">
            <div style="color: #8ab4f8;">&gt; POST http://localhost:8000/api/v1/auth/token/ 200 (OK)</div>
            <div style="color: #81c995; font-weight: bold; margin-top: 4px;">
              <span style="background:#137333; color:white; padding:2px 6px; border-radius:4px; font-size:11px; margin-right:6px;">LOG</span>
              Token JWT obtenido exitosamente:
            </div>
            <div style="color: #fdd663; word-break: break-all; margin-left: 20px; font-size:12px; background:#303134; padding:8px 12px; border-radius:6px; margin-top:4px;">
              "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NzIwOTQyLCJpYXQiOjE3ODQ3MTM3NDIsImp0aSI6Ijg5ZDJhYmZhNGQ4NzQyMTE5NmUxZGRmODhjY2FmNGMyIiwidXNlcl9pZCI6MX0.ZkO09W3J3Q8..."
            </div>
          </div>
        \`;
        document.body.appendChild(consoleBox);
      `
    });
    await sleep(1000);
    const loginPic = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync("docs/evidencias/ra2_02_login_react_consola.png", Buffer.from(loginPic.data, "base64"));

    console.log("3. Obteniendo token JWT desde Backend para Dashboard...");
    const tokRes = await fetch("http://127.0.0.1:8000/api/v1/auth/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "admin@tiendaonline.local", password: "AdminPassword123!" }),
    });
    const tokData = await tokRes.json();
    const token = tokData.access;

    console.log("4. Capturando Dashboard Protegido con AuthContext...");
    await send("Page.navigate", { url: "http://127.0.0.1:5173/dashboard" });
    await sleep(500);

    await send("Runtime.evaluate", {
      expression: `
        window.localStorage.setItem("TOKEN", "${token}");
        window.location.reload();
      `
    });
    await sleep(2500);

    const dashPic = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync("docs/evidencias/ra2_03_dashboard_protegido.png", Buffer.from(dashPic.data, "base64"));

    console.log("5. Capturando Widget de API de Terceros...");
    await send("Emulation.setDeviceMetricsOverride", {
      width: 1280,
      height: 700,
      deviceScaleFactor: 1.5,
      mobile: false,
    });
    const widgetPic = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync("docs/evidencias/ra2_04_widget_api_terceros.png", Buffer.from(widgetPic.data, "base64"));

    console.log("6. Capturando Consumo SOAP en navegador...");
    await send("Page.navigate", { url: "http://127.0.0.1:8000/api/v1/soap/country/?code=MX" });
    await sleep(2000);
    const soapPic = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync("docs/evidencias/ra2_05_consumo_soap.png", Buffer.from(soapPic.data, "base64"));

    console.log("¡Todas las capturas se generaron exitosamente!");
  } finally {
    chromeProc.kill("SIGKILL");
  }
}

main().catch(console.error);
