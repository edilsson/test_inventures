import React, { useEffect, useState } from 'react';
import Shortener from "./components/Shortener";
import Stats from "./components/Stats";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const App = () => (
  <Container fluid="md">
    <Row className="py-5">
      <h1 className="header">Inventures URL Shortener</h1>
    </Row>
    <Row>
      <Shortener />
    </Row>
    <Row>
      <Stats />
    </Row>
  </Container>
);

export default App;
