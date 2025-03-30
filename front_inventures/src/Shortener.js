import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';


const API_SHORTENER = "http://localhost:8000/shorten"

export default function Shortener() {
    const [url, setUrl] = useState("");
    const [customAlias, setCustomAlias] = useState("");
    const [result, setResult] = useState("");
    const [message, setMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const urlData = { url, custom_alias: customAlias };

        try {
            const response = await fetch(API_SHORTENER, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(urlData),
            });
            console.log(response);
            if (!response.ok) throw new Error("There was an error trying to shorten the URL");    
            const result = await response.json();
            console.log(result);

            setResult(`Shortened URL: ${"http://localhost:8000/" + result.alias}`);
        } catch (error) {
            console.log(error);
            setMessage(error.message);
        }
    };

    return (
        <div className="mx-auto">
            <Form onSubmit={handleSubmit} className="mb-4">
                <Form.Group className="mb-3" controlId="url">
                    <Form.Control
                        type="text"
                        placeholder="URL (http://...)"
                        value={url}
                        required
                        onChange={(e) => setUrl(e.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3" controlId="custom_alias">
                    <Form.Control
                        type="text"
                        placeholder="Custom Alias"
                        value={customAlias}
                        onChange={(e) => setCustomAlias(e.target.value)}
                    />
                </Form.Group>
                <Button as="input" variant="dark" size="lg" type="submit" value="Shorten!" />
            </Form>
        </div>
    );
}