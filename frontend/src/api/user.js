const API_URL = import.meta.env.VITE_BASE_API_URL || "http://localhost:8000";

export async function loginApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/token/`;
    const params = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };
    const response = await fetch(url, params);
    if (response.status !== 200) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || "Usuario o contraseña incorrecta");
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}

export async function registerApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/register/`;
    const params = {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };
    const response = await fetch(url, params);
    if (response.status !== 201) {
      const errData = await response.json().catch(() => ({}));
      const firstError = Object.values(errData)[0];
      const message = Array.isArray(firstError) ? firstError[0] : (typeof firstError === 'string' ? firstError : "No se pudo registrar el usuario");
      throw new Error(message);
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}

export async function getMeApi(token) {
  try {
    const url = `${API_URL}/api/v1/auth/me/`;
    const params = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
    const response = await fetch(url, params);
    if (response.status !== 200) {
      throw new Error("Error al obtener los datos del usuario");
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}
