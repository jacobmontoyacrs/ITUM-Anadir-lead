from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

@app.route('/addLead', methods=['POST'])
def add_lead():
    incoming = request.get_json()

    # Extraer todos los campos esperados
    nombre = incoming.get("nombre")
    telefono = incoming.get("telefono")
    email = incoming.get("email")
    tipo_cliente = incoming.get("tipoCliente")
    producto_interes = incoming.get("productoInteres")
    direccion = incoming.get("direccion")
    sucursal = incoming.get("sucursal")
    resumen = incoming.get("resumen")

    # Validación básica del campo obligatorio
    if not nombre:
        return jsonify({"error": "Falta el campo 'nombre' en el cuerpo"}), 400

    # URL del flujo de Power Automate
    power_url = "https://c0dadb8d5cc6e1b8ac840efb29924c.06.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/e9665837831b401883665783ebf3bf79/triggers/manual/paths/invoke/?api-version=1&tenantId=tId&environmentName=c0dadb8d-5cc6-e1b8-ac84-0efb29924c06&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Nh0xYPKzEU9I9Xg5crsYdTvoIn4blyGlQew6gRvluro"

    headers = {
        "Content-Type": "application/json"
    }

    # Cuerpo que se enviará al flujo
    data = {
        "nombre": nombre,
        "telefono": telefono,
        "email": email,
        "tipoCliente": tipo_cliente,
        "productoInteres": producto_interes,
        "direccion": direccion,
        "sucursal": sucursal,
        "resumen": resumen
    }

    # Llamar al flujo
    response = requests.post(power_url, headers=headers, data=json.dumps(data))

    return jsonify({
        "status": response.status_code,
        "flow_response": response.text
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
