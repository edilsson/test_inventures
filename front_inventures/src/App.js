import React, { useEffect, useState } from 'react';
import Shortener from "./Shortener";

import Toast from 'react-bootstrap/Toast';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Nav from 'react-bootstrap/Nav';
import Table from 'react-bootstrap/Table';

const App = () => (
  <Container fluid className="p-5">
    <h1 className="header">Inventures URL Shortener</h1>
    <Row>
        <Shortener />
    </Row>
    <Row>
      <Col>b
      </Col>
      <Col>c
      </Col>
    </Row>
  </Container>
);

export default App;
