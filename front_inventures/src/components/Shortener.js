import React, { useState } from 'react';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';


const API_SHORTENER = "http://0.0.0.0:8000/shorten"

export default function Shortener() {
    const [url, setUrl] = useState("");
    const [customAlias, setCustomAlias] = useState("");
    const [result, setResult] = useState("");
    const [alertType, setAlertType] = useState("");
    const [showAlert, setShowAlert] = useState(null);
    const currentHost = `${window.location.protocol}//${window.location.hostname}`;

    const handleSubmit = async (e) => {
        e.preventDefault();
        const urlData = { url, custom_alias: customAlias };

        try {
            const response = await fetch(API_SHORTENER, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(urlData),
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.detail);
            }

            setResult(`Shortened URL: ${currentHost + ":8000/" + result.alias}`);
            setAlertType("success");
            setShowAlert(true);
        } catch (error) {
            setResult(error.message);
            setAlertType("danger");
            setShowAlert(true);
        }
    };

    return (
        <>
        <Row>
            <Col>
            <h3>Insert the URL you want to shorten and a custom alias if you want to.</h3>
            </Col>
        </Row>
        <Row>
            <Form onSubmit={handleSubmit} className="mb-4">
                <Row>
                    <Col lg={7}>
                        <Form.Group className="mb-3" controlId="url">
                            <Form.Control
                                size="lg"
                                type="url"
                                placeholder="URL (http://...)"
                                value={url}
                                required
                                onChange={(e) => setUrl(e.target.value)}
                            />
                        </Form.Group>
                    </Col>
                    <Col lg={3}>
                        <Form.Group className="mb-3" controlId="custom_alias">
                            <Form.Control
                                size="lg"
                                type="text"
                                placeholder="Custom Alias"
                                value={customAlias}
                                onChange={(e) => setCustomAlias(e.target.value)}
                            />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Button as="input" variant="dark" size="lg" type="submit" value="Shorten!" />
                    </Col>
                </Row>
            </Form>
        </Row>
        <Row>
        {
            showAlert ? 
                <Alert key={alertType} variant={alertType} onClose={() => setShowAlert(false)} dismissible>
                    {result}
                </Alert>
                :
                ""
        }
        </Row>
        </>
    );
}