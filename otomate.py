import os
import subprocess
import time
import schedule

# Doğru dosya yolları
vavoo_script = r"C:\Users\ACK\Desktop\,\pyt\vavookooloha\templates\Vavoo_m3u.py"
duzenleyici_script = r"C:\Users\ACK\Desktop\,\pyt\vavooDuzenleyici\vavooDuzenleyici.py"
m3u_file = r"C:\Users\ACK\Desktop\,\patronvavoo\link\vavoo.m3u"
repo_path = r"C:\Users\ACK\Desktop\patronvavoo"  # Git deposunun ana klasörü

def run_vavoo_scraper():
    print("Vavoo yayınlarını çekme işlemi başladı...")
    subprocess.run(["python", vavoo_script], check=True)
    print("Vavoo yayınlarını çekme işlemi tamamlandı.")

def run_formatter():
    print("Listeyi formatlama işlemi başladı...")
    subprocess.run(["python", duzenleyici_script], check=True)
    print("Listeyi formatlama işlemi tamamlandı.")

def push_to_github():
    print("Git işlemleri başladı...")

    # Git deposunun içine gir
    os.chdir(repo_path)

    # Git işlemleri
    subprocess.run(["git", "add", "vavoo.m3u"], check=True)
    subprocess.run(["git", "commit", "-m", "Otomatik güncelleme"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

    print("Git işlemleri tamamlandı.")

def automate_process():
    run_vavoo_scraper()
    run_formatter()
    push_to_github()

# 5 saatte bir çalıştır
schedule.every(5).hours.do(automate_process)

automate_process()  # İlk başlatmada çalıştır

while True:
    schedule.run_pending()
    time.sleep(60)  # Her dakika kontrol et
