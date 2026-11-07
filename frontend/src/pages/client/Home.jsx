import React from "react";
import { Link } from "react-router-dom";
import { Button, Container, Header, Segment, Icon } from "semantic-ui-react";

export function Home() {
  return (
    <Container style={{ paddingTop: "60px", textAlign: "center" }}>
      <Segment placeholder raised>
        <Header icon>
          <Icon name="shopping bag" color="teal" />
          Tienda Online — Portal Full Stack
          <Header.Subheader style={{ marginTop: "10px" }}>
            Arquitectura desacoplada: Django REST Framework + JWT + React + Semantic UI
          </Header.Subheader>
        </Header>
        <Segment.Inline style={{ marginTop: "20px" }}>
          <Button as={Link} to="/login" primary size="large">
            <Icon name="sign-in" /> Iniciar Sesión
          </Button>
          <Button as={Link} to="/register" secondary size="large">
            <Icon name="user plus" /> Registrarse
          </Button>
          <Button as={Link} to="/dashboard" color="teal" size="large">
            <Icon name="dashboard" /> Ir al Dashboard
          </Button>
        </Segment.Inline>
      </Segment>
    </Container>
  );
}
