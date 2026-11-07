import React from "react";
import { Link } from "react-router-dom";
import { Button, Container, Header, Icon, Segment } from "semantic-ui-react";

export function Error404() {
  return (
    <Container style={{ paddingTop: "80px", textAlign: "center" }}>
      <Segment placeholder>
        <Header icon>
          <Icon name="exclamation triangle" color="red" />
          Página no encontrada (Error 404)
        </Header>
        <Button as={Link} to="/" primary>
          Volver al Inicio
        </Button>
      </Segment>
    </Container>
  );
}

export default Error404;
