import requests
import re

# Vavoo içeriğini yerel dosyadan okumak için, ana dizindeki sabit dosyamızın adını ekleyelim
def fetch_vavoo_content():
    # vavoo.m3u dosyasından içeriği al
    with open('vavoo.m3u', 'r', encoding='utf-8') as f:
        return f.read()

# Kanal etiketlerini ve bilgilerini ayıralım
def parse_channel(lines, start_idx):
    if start_idx >= len(lines):
        return None, start_idx
    
    # Kanal bilgilerini aldığımız yöntem
    channel = {
        'extinf': '',        # Kanal meta bilgileri
        'user_agent': '',    # User agent bilgisi
        'referrer': '',      # Referans URL
        'url': ''            # Akışın URL Adresi
    }
    
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF'):
            # TVG-ID etiketi kalsın ve grup başlığını kanal grubuna göre otomatik değiştirelim
            tvg_id_match = re.search('tvg-id="([^"]*)"', line)
            tvg_id = tvg_id_match.group(1) if tvg_id_match else ''
            
            # Grup başlığını düzenle
            if is_sports_channel({'extinf': line}):
                group = 'Türkiye/Bein ve Spor Kanalları'
            elif is_news_channel({'extinf': line}):
                group = 'Türkiye/Haber'
            elif is_kids_channel({'extinf': line}):
                group = 'Türkiye/Çocuk'
            elif is_movie_channel({'extinf': line}):
                group = 'Türkiye/Film'
            else:
                group = 'Türkiye/Genel'
                
            # Logo URL'sini ekle
            if 'tvg-logo=""' in line or 'tvg-logo=' not in line:
                line = re.sub('tvg-logo="[^"]*"', 'tvg-logo="https://raw.githubusercontent.com/patr0nq/link/refs/heads/main/tv-logo/tv-logo.png"', line)
                if 'tvg-logo=' not in line:
                    line = line.replace('group-title=', 'tvg-logo="https://raw.githubusercontent.com/patr0nq/link/refs/heads/main/tv-logo/tv-logo.png" group-title=')
            
            # Yeni EXTINF satırını oluştur
            line = re.sub('group-title="[^"]*"', f'group-title="{group}"', line)
            if 'tvg-language=' not in line:
                line = line.replace('group-title=', 'tvg-language="Turkish" tvg-country="TR" group-title=')
            channel['extinf'] = line
        elif line.startswith('#EXTVLCOPT:http-user-agent'):
            channel['user_agent'] = line
        elif line.startswith('#EXTVLCOPT:http-referrer'):
            channel['referrer'] = line
        elif line.startswith('http'):
            channel['url'] = line
            return channel, i + 1
        i += 1
    
    return None, i

# Bein kanalları ve Spor kanalları kontrolü
def is_sports_channel(channel):
    # Spor kanallarını belirlemek için anahtar kelimeler
    sports_keywords = ['SPORT', 'SPOR', 'EUROSPORT', 'NBA TV', 'S SPORT', 'TIVIBU SPOR', 
                      'FB TV', 'GS TV', 'BJK TV', 'TRT SPOR', 'A SPOR', 'SPORTS TV']
    channel_name = channel['extinf'].upper()
    
# Bein kanallarını almayı sonraya bırakıyoruz sadece spor içerikli kanalları alıyoruz.
# Bein kanalları için özel kontrol. Kanal adında Bein geçiyorsa hepsini almak için.
#    if 'BEIN' in channel_name:
#        return True
    
    return any(keyword in channel_name for keyword in sports_keywords)

# Haber kanalı kontrolü
def is_news_channel(channel):
    # Haber kanallarını belirlemek için anahtar kelimeler
    news_keywords = ['HABER', 'NEWS', 'CNN', 'BBC', 'NTV', 'BLOOMBERG', 'HABERTURK', 'A HABER', 
                    'TRT HABER', 'ULKE', 'TGRT', '24', 'GLOBAL']
    return any(keyword in channel['extinf'].upper() for keyword in news_keywords)

# Çocuk kanalı kontrolü
def is_kids_channel(channel):
    # Çocuk kanallarını belirlemek için anahtar kelimeler
    kids_keywords = ['CARTOON', 'DISNEY', 'NICKELODEON', 'NICK JR', 'BABY', 'COCUK', 'TRT COCUK', 'MINIKA',
                    'BOOMERANG', 'DUCK TV', 'DA VINCI', 'CBEEBIES', 'CARTOONITO']
    return any(keyword in channel['extinf'].upper() for keyword in kids_keywords)

# Film kanalı kontrolü
def is_movie_channel(channel):
    # Film ve dizi kanallarını belirlemek için anahtar kelimeler
    movie_keywords = ['MOVIE', 'FILM', 'CINEMA', 'SINEMA', 'DIZI', 'SERIES', 'FX', 'COMEDY', 
                     'ACTION', 'DRAMA', 'PREMIUM', 'MAX', 'GOLD', 'PLATIN', '+', 'SMART', 'BOX']
    return any(keyword in channel['extinf'].upper() for keyword in movie_keywords)

# M3U dosyası oluştur
def write_m3u_file(filename, channels):
    # kekik-vavoo dizinini oluştur (eğer yoksa)
    import os
    output_dir = 'kekik-vavoo'
    os.makedirs(output_dir, exist_ok=True)
    
    # Dosyayı kekik-vavoo dizininde oluştur
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for channel in channels:
            f.write(f"{channel['extinf']}\n")
            f.write(f"{channel['user_agent']}\n")
            f.write(f"{channel['referrer']}\n")
            f.write(f"{channel['url']}\n")

# Ana fonksiyon
def main():
    # Vavoo içeriğini al ve satırlara böl
    content = fetch_vavoo_content()
    lines = content.split('\n')
    
    # Kanal kategorileri için listeler
    sports_channels = []  # Spor kanalları
    news_channels = []    # Haber kanalları
    kids_channels = []    # Çocuk kanalları
    movie_channels = []   # Film ve dizi kanalları
    other_channels = []   # Diğer kanallar
    
    # Kanalları kategorilere ayır
    idx = 0
    while idx < len(lines):
        channel, new_idx = parse_channel(lines, idx)
        if channel:
            if is_sports_channel(channel):
                sports_channels.append(channel)
            elif is_news_channel(channel):
                news_channels.append(channel)
            elif is_kids_channel(channel):
                kids_channels.append(channel)
            elif is_movie_channel(channel):
                movie_channels.append(channel)
            else:
                other_channels.append(channel)
        idx = new_idx
    
    # Kanalları isimlerine göre sırala
    for channel_list in [sports_channels, news_channels, kids_channels, movie_channels, other_channels]:
        channel_list.sort(key=lambda x: x['extinf'])
    
    # Kategorilere göre M3U dosyalarını oluştur
    write_m3u_file('vavoo-sadecespor.m3u', sports_channels)    # Spor kanalları (Bein dahil)
    write_m3u_file('vavoo-haber.m3u', news_channels)      # Haber kanalları
    write_m3u_file('vavoo-cocuk.m3u', kids_channels)      # Çocuk kanalları
    write_m3u_file('vavoo-film.m3u', movie_channels)      # Film ve dizi kanalları
    write_m3u_file('vavoo-genel.m3u', other_channels)     # Diğer kanallar

if __name__ == '__main__':
    main()
