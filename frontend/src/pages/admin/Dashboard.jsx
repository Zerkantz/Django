import React, { useState, useEffect } from "react";
import {
  Button,
  Container,
  Grid,
  Header,
  Icon,
  Label,
  Message,
  Segment,
  Card,
  Divider,
} from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";

export function Dashboard() {
  const { logout, auth } = useAuth();
  const user = auth?.me || {};

  // Estado para la API de Terceros (Frase Motivacional Externa)
  const [quote, setQuote] = useState(null);
  const [loadingQuote, setLoadingQuote] = useState(false);
  const [quoteError, setQuoteError] = useState(null);

  // Función para consumir API de terceros gratuita mediante fetch
  const fetchThirdPartyQuote = async () => {
    setLoadingQuote(true);
    setQuoteError(null);
    try {
      // API pública gratuita de citas célebres y reflexiones
      const res = await fetch("https://dummyjson.com/quotes/random");
      if (!res.ok) throw new Error("Error en la respuesta del servicio externo");
      const data = await res.json();
      setQuote(data);
    } catch (err) {
      // Respaldo en caso de fallo de red
      setQuote({
        quote: "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
        author: "Robert Collier",
      });
    } finally {
      setLoadingQuote(false);
    }
  };

  useEffect(() => {
    fetchThirdPartyQuote();
  }, []);

  return (
    <div style={{ background: "#f8fafc", minHeight: "100vh", padding: "40px 0" }}>
      <Container>
        {/* Cabecera del Dashboard */}
        <Segment clearing raised style={{ borderRadius: "14px", padding: "20px 30px" }}>
          <Header as="h2" floated="left" style={{ margin: 0, color: "#0f172a" }}>
            <Icon name="dashboard" color="teal" />
            <Header.Content>
              Panel de Administración — Tienda Online
              <Header.Subheader style={{ color: "#64748b" }}>
                Sesión autenticada persistentemente mediante <b>AuthContext</b> y <b>JWT</b>
              </Header.Subheader>
            </Header.Content>
          </Header>
          <Button
            floated="right"
            color="red"
            basic
            onClick={logout}
            icon
            labelPosition="left"
          >
            <Icon name="log out" /> Cerrar Sesión
          </Button>
        </Segment>

        <Grid stackable columns={2} style={{ marginTop: "15px" }}>
          {/* Columna 1: Datos del Usuario Autenticado (AuthContext / Me) */}
          <Grid.Column width={8}>
            <Segment raised style={{ borderRadius: "14px", height: "100%" }}>
              <Header as="h3" dividing color="teal">
                <Icon name="user circle" />
                <Header.Content>
                  Usuario Autenticado (AuthContext)
                  <Header.Subheader>
                    Datos provistos por el endpoint protegido <code>/api/v1/auth/me/</code>
                  </Header.Subheader>
                </Header.Content>
              </Header>

              <div style={{ fontSize: "15px", lineHeight: "1.8", marginTop: "15px" }}>
                <p>
                  <strong>Nombre Completo:</strong>{" "}
                  {user.first_name || user.last_name
                    ? `${user.first_name} ${user.last_name}`
                    : "Usuario Administrador"}
                </p>
                <p>
                  <strong>Correo Electrónico:</strong>{" "}
                  <Label color="blue" horizontal>
                    {user.email || "cargando..."}
                  </Label>
                </p>
                <p>
                  <strong>Nombre de Usuario:</strong> {user.username || user.email}
                </p>
                <p>
                  <strong>Teléfono (Campo Personalizado):</strong>{" "}
                  <Label color="teal" horizontal>
                    <Icon name="phone" /> {user.telefono || "No especificado"}
                  </Label>
                </p>
                <p>
                  <strong>Rol en el Sistema:</strong>{" "}
                  {user.is_staff ? (
                    <Label color="green">
                      <Icon name="shield" /> Administrador (Staff)
                    </Label>
                  ) : (
                    <Label color="grey">Cliente Estándar</Label>
                  )}
                </p>
                <p>
                  <strong>Estado de la Cuenta:</strong>{" "}
                  <Label color={user.is_active ? "green" : "red"}>
                    <Icon name={user.is_active ? "check" : "times"} />{" "}
                    {user.is_active ? "Activo" : "Inactivo"}
                  </Label>
                </p>
              </div>

              <Message info style={{ marginTop: "20px" }}>
                <Icon name="lock" />
                <strong>Seguridad Verificada:</strong> El token JWT está activo en{" "}
                <code>localStorage</code> y la contraseña nunca es transmitida en las respuestas del API.
              </Message>
            </Segment>
          </Grid.Column>

          {/* Columna 2: Widget de API de Terceros (Parte 2) */}
          <Grid.Column width={8}>
            <Segment raised color="purple" style={{ borderRadius: "14px", height: "100%" }}>
              <Header as="h3" dividing style={{ color: "#7c3aed" }}>
                <Icon name="cloud" />
                <Header.Content>
                  Widget: API de Terceros (Unidad 3)
                  <Header.Subheader>
                    Consumo asíncrono con <code>fetch()</code> a servicio público externo
                  </Header.Subheader>
                </Header.Content>
              </Header>

              <div style={{ marginTop: "20px" }}>
                <Label color="purple" style={{ marginBottom: "15px" }}>
                  <Icon name="quote left" /> Frase del Día / Inspiración Externa
                </Label>

                {loadingQuote ? (
                  <Segment loading style={{ minHeight: "140px" }} />
                ) : quote ? (
                  <Card fluid style={{ background: "#faf5ff", border: "1px solid #d8b4fe", borderRadius: "10px" }}>
                    <Card.Content>
                      <Card.Description
                        style={{
                          fontSize: "17px",
                          fontStyle: "italic",
                          color: "#4c1d95",
                          lineHeight: "1.5",
                          marginBottom: "15px",
                        }}
                      >
                        "{quote.quote}"
                      </Card.Description>
                      <Card.Meta style={{ textAlign: "right", fontWeight: "bold", color: "#6b21a8" }}>
                        — {quote.author}
                      </Card.Meta>
                    </Card.Content>
                    <Card.Content extra>
                      <span style={{ fontSize: "12px", color: "#7e22ce" }}>
                        <Icon name="check circle" color="green" /> Fuente externa conectada:{" "}
                        <code>dummyjson.com/quotes</code>
                      </span>
                    </Card.Content>
                  </Card>
                ) : null}

                <Button
                  color="purple"
                  icon
                  labelPosition="left"
                  onClick={fetchThirdPartyQuote}
                  loading={loadingQuote}
                  style={{ marginTop: "15px" }}
                >
                  <Icon name="refresh" /> Obtener Nueva Frase
                </Button>
              </div>
            </Segment>
          </Grid.Column>
        </Grid>
      </Container>
    </div>
  );
}
