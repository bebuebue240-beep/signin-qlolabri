import urllib.request, json
TOKEN = '9010856651:AAEiA6atsNwoC9drL1UouSg27SP_n9p_3Yk'
CHAT_ID = '8555026746'
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
req = urllib.request.Request(url, data=json.dumps({"chat_id": CHAT_ID, "text": "Tes Koneksi Termux"}).encode(), headers={'Content-Type': 'application/json'})
try:
    urllib.request.urlopen(req)
    print("✅ BERHASIL! Cek Telegram Anda.")
except Exception as e:
    print("❌ GAGAL. Error:", e)
