import os
import time
import schedule

# Doğru dosya yolları
vavoo_script = r"C:\Users\ACK\Desktop\pyt\vavookooloha\templates\Vavoo_m3u.py"
duzenleyici_script = r"C:\Users\ACK\Desktop\pyt\vavooDuzenleyici\vavooDuzenleyici.py"
m3u_file = r"C:\Users\ACK\Desktop\patronvavoo\link\vavoo.m3u"
repo_path = r"C:\Users\ACK\Desktop\patronvavoo"  # Git deposunun ana klasörü

def run_vavoo_scraper():
    print("Vavoo yayınlarını çekme işlemi başladı...")
    os.system(f"python {vavoo_script}")
    print("Vavoo yayınlarını çekme işlemi tamamlandı.")

def run_formatter():
    print("Listeyi formatlama işlemi başladı...")
    os.system(f"python {duzenleyici_script}")
    print("Listeyi formatlama işlemi tamamlandı.")

def push_to_github():
    print("Git işlemleri başladı...")

    # Git deposuna geç
    os.chdir(repo_path)

    # Git işlemlerini sırayla çalıştır
    os.system("git reset --hard")  # Değişiklikleri sıfırla
    os.system("git pull --rebase")  # Uzak repo ile senkronize ol

    if os.path.exists(m3u_file):
        os.system("git add .")
        os.system('git commit -m "Otomatik güncelleme"')
        os.system("git push origin main")
        print("Git işlemleri tamamlandı.")
    else:
        print("HATA: vavoo.m3u dosyası bulunamadı!")

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
