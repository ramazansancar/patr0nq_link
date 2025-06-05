import requests

source_url = "https://lemonchiffon-dotterel-347603.hostingersite.com/kablotv/kablotv.m3u"
target_path = "sakultah.m3u"

response = requests.get(source_url)

if response.status_code == 200:
    lines = response.text.splitlines()
    filtered_lines = []

    for line in lines:
        line = line.strip()  # Satır başı ve sonu boşlukları temizle

        if not line:  # Boş satırları atla
            continue

        if line.startswith("#EXTINF:"):
            if "tvg-language=" not in line and "tvg-country=" not in line:
                line = line.replace('#EXTINF:-1', '#EXTINF:-1 tvg-language="Turkish" tvg-country="TR"')
            filtered_lines.append(line)
        else:
            filtered_lines.append(line)  # Link satırları da dahil et (temizlenmiş haliyle)

    # Başta #EXTM3U yoksa ekle
    if not filtered_lines or not filtered_lines[0].startswith("#EXTM3U"):
        filtered_lines.insert(0, "#EXTM3U")

    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered_lines))

    print(f"Liste başarıyla '{target_path}' olarak kaydedildi.")
else:
    print(f"Kaynak M3U alınamadı. Status code: {response.status_code}")
