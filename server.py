from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# WhatsApp notification via CallMeBot or similar
WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '254722816001')
WHATSAPP_API_KEY = os.environ.get('WHATSAPP_API_KEY', '')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    name = data.get('name', '')
    phone = data.get('phone', '')
    product = data.get('product', '')
    message = data.get('message', '')

    # Format WhatsApp message
    wa_message = (
        f"🛒 *New Order - Nexcom Limited*\n\n"
        f"👤 *Name:* {name}\n"
        f"📞 *Phone:* {phone}\n"
        f"💻 *Product:* {product}\n"
        f"💬 *Message:* {message}"
    )

    # Send via CallMeBot WhatsApp API
    if WHATSAPP_API_KEY:
        try:
            url = f"https://api.callmebot.com/whatsapp.php?phone={WHATSAPP_NUMBER}&text={requests.utils.quote(wa_message)}&apikey={WHATSAPP_API_KEY}"
            requests.get(url, timeout=10)
        except Exception as e:
            print(f"WhatsApp notification error: {e}")

    return jsonify({"status": "ok", "message": "Order received! We'll contact you shortly."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
