#!/bin/bash

# Inicia el servidor Flask en segundo plano
python3  app/routes.py &

# Espera un tiempo para asegurarse de que el servidor Flask esté en funcionamiento
sleep 10

# Realiza la solicitud curl al servidor Flask
curl -X POST -H "Content-Type: application/json" -d @cufes.json http://localhost:5000/api/v1/consult_invoice_information
