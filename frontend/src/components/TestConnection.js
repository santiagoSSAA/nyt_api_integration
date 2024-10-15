import React, { useEffect, useState } from 'react';

const TestConnection = () => {
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchTestConnection = async () => {
            try {
                const url = `${process.env.REACT_APP_BACKEND_URL}`;
                const response = await fetch(url);
                if (response.ok) {
                    const data = await response.json();
                    setMessage(data.message);
                } else {
                    setMessage('Error en la conexión: ' + response.status + ' ' + response.statusText);
                }
            } catch (error) {
                setMessage('Error al realizar la solicitud: ' + error.message);
            }
        };

        fetchTestConnection();
    }, []);

    return (
        <div>
            <h1>Prueba de Conexión</h1>
            <p>{message}</p>
        </div>
    );
};

export default TestConnection;
