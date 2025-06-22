from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

@app.route('/addLead', methods=['POST'])
def add_lead():
    incoming = request.get_json()
    name = incoming.get("name")

    if not name:
        return jsonify({"error": "Falta el campo 'name' en el cuerpo"}), 400

    # URL de tu flujo Power Automate (¡incluye el ?sig=... completo!)
    power_url = "https://c0dadb8d5cc6e1b8ac840efb29924c.06.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/e9665837831b401883665783ebf3bf79/triggers/manual/paths/invoke/?api-version=1&tenantId=tId&environmentName=c0dadb8d-5cc6-e1b8-ac84-0efb29924c06&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Nh0xYPKzEU9I9Xg5crsYdTvoIn4blyGlQew6gRvluro"

    headers = {
        "Content-Type": "application/json"
    }

    data = { "name": name }

    response = requests.post(power_url, headers=headers, data=json.dumps(data))

    return jsonify({
        "status": response.status_code,
        "flow_response": response.text
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ← usa el puerto dinámico que Render proporciona
    app.run(host="0.0.0.0", port=port)
