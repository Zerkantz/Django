import React, { useState } from "react";
import { Button, Form, Message } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";
import { loginApi } from "../../api/user";
import { useAuth } from "../../hooks/useAuth";

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    onSubmit: async (formValues) => {
      setLoading(true);
      try {
        const response = await loginApi(formValues);
        const { access } = response;
        console.log("Token JWT obtenido exitosamente:", access);
        toast.success("¡Inicio de sesión exitoso!");
        await login(access);
        navigate("/dashboard");
      } catch (error) {
        toast.error(error.message || "Error al iniciar sesión");
      } finally {
        setLoading(false);
      }
    },
  });

  return (
    <div className="login-admin">
      <div className="login-admin__content">
        <h1>Iniciar Sesión</h1>
        <p style={{ textAlign: "center", color: "#64748b", marginTop: "-30px", marginBottom: "30px" }}>
          Tienda Online — Autenticación JWT
        </p>
        <Form className="login-form-admin" onSubmit={formik.handleSubmit}>
          <label>Correo electrónico</label>
          <Form.Input
            name="email"
            placeholder="ejemplo@tiendaonline.local"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.email}
          />
          <label>Contraseña</label>
          <Form.Input
            name="password"
            type="password"
            placeholder="••••••••"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.errors.password}
            autoComplete="current-password"
          />
          <Button
            type="submit"
            content="Ingresar al Sistema"
            primary
            fluid
            loading={loading}
          />
        </Form>
        <div style={{ marginTop: "24px", textAlign: "center" }}>
          <span>¿No tienes una cuenta aún? </span>
          <Link to="/register" style={{ fontWeight: "bold", color: "#0098d3" }}>
            Regístrate aquí
          </Link>
        </div>
      </div>
    </div>
  );
}

function initialValues() {
  return {
    email: "",
    password: "",
  };
}

function validationSchema() {
  return Yup.object({
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    password: Yup.string().required("La contraseña es obligatoria"),
  });
}
