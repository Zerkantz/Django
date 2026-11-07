import React, { useState } from "react";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";
import { registerApi } from "../../api/user";

export function Register() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    onSubmit: async (formValues) => {
      setLoading(true);
      try {
        await registerApi(formValues);
        toast.success("¡Usuario registrado exitosamente! Ahora puedes iniciar sesión.");
        navigate("/login");
      } catch (error) {
        toast.error(error.message || "Error al registrar el usuario");
      } finally {
        setLoading(false);
      }
    },
  });

  return (
    <div className="register-admin">
      <div className="register-admin__content">
        <h1>Registro de Usuario</h1>
        <p style={{ textAlign: "center", color: "#64748b", marginTop: "-30px", marginBottom: "30px" }}>
          Crea tu cuenta en Tienda Online
        </p>
        <Form className="register-form-admin" onSubmit={formik.handleSubmit}>
          <label>Nombre de usuario</label>
          <Form.Input
            name="username"
            placeholder="usuario123"
            value={formik.values.username}
            onChange={(e) => {
              const value = e.target.value.replace(/\s+/g, "");
              formik.setFieldValue("username", value);
            }}
            onBlur={formik.handleBlur}
            error={formik.errors.username}
          />

          <label>Correo electrónico</label>
          <Form.Input
            name="email"
            placeholder="correo@ejemplo.com"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.email}
          />

          <label>Teléfono (Campo extra)</label>
          <Form.Input
            name="telefono"
            placeholder="667-123-4567"
            value={formik.values.telefono}
            onChange={formik.handleChange}
            error={formik.errors.telefono}
          />

          <label>Contraseña</label>
          <Form.Input
            name="password"
            type="password"
            placeholder="Mínimo 8 caracteres, mayúscula, número y símbolo"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.errors.password}
            autoComplete="new-password"
          />

          <label>Confirmar Contraseña</label>
          <Form.Input
            name="password_confirm"
            type="password"
            placeholder="Repite tu contraseña"
            value={formik.values.password_confirm}
            onChange={formik.handleChange}
            error={formik.errors.password_confirm}
            autoComplete="new-password"
          />

          <Button
            type="submit"
            content="Registrarse"
            primary
            fluid
            loading={loading}
          />
        </Form>
        <div style={{ marginTop: "24px", textAlign: "center" }}>
          <span>¿Ya tienes una cuenta? </span>
          <Link to="/login" style={{ fontWeight: "bold", color: "#0098d3" }}>
            Inicia sesión aquí
          </Link>
        </div>
      </div>
    </div>
  );
}

function initialValues() {
  return {
    username: "",
    email: "",
    telefono: "",
    password: "",
    password_confirm: "",
  };
}

function validationSchema() {
  return Yup.object({
    username: Yup.string()
      .required("El nombre de usuario es obligatorio")
      .matches(/^\S*$/, "El username no debe contener espacios"),
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    telefono: Yup.string(),
    password: Yup.string()
      .required("La contraseña es obligatoria")
      .min(8, "La contraseña debe tener al menos 8 caracteres")
      .matches(/[A-Z]/, "Debe contener al menos una letra mayúscula")
      .matches(/\d/, "Debe contener al menos un número")
      .matches(/[@$!%*?&#.]/, "Debe contener al menos un carácter especial (@$!%*?&#.)"),
    password_confirm: Yup.string()
      .required("La confirmación de contraseña es obligatoria")
      .oneOf([Yup.ref("password"), null], "Las contraseñas no coinciden"),
  });
}
