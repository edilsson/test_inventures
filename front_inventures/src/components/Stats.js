import React from 'react';
import fetchData from "../fetchData";
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Table from 'react-bootstrap/Table';

const currentHost = `${window.location.protocol}//${window.location.hostname}`;
const API_STATS = currentHost + ":8000/stats"

export default function Stats() {
    const { data, loading, error } = fetchData(API_STATS);
    
    const columns = [
        { label: "URL", accessor: "original_url" },
        { label: "Alias", accessor: "alias" },
        { label: "Created at (UTC)", accessor: "created_at" },
        { label: "# Clicks", accessor: "clicks" },
    ];

    if (loading) return <p className="text-center p-4">Loading...</p>;
    if (error) return <p className="text-center p-4 text-red-500">{error}</p>;

    return (
        <>
            <Row>
                <Col>
                    <h5>Shortened URLs</h5>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                {columns.map(({ label, accessor }) => (
                                    <th key={accessor}>{label}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((urlData) => (
                            <tr key={urlData.alias}>
                                <td>{urlData.original_url}</td>
                                <td>{urlData.alias}</td>
                                <td>{urlData.created_at}</td>
                                <td>{urlData.clicks}</td>
                            </tr>
                            ))}
                        </tbody>
                    </Table>
                </Col>
            </Row>
        </>
    );
};