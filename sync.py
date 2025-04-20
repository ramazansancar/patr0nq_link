import requests

source_url = "https://raw.githubusercontent.com/DRAG-10/DRAG10/refs/heads/special/DRAG10.m3u"
target_path = "dragon.m3u"

response = requests.get(source_url)

if response.status_code == 200:
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(response.text)
else:
    print(f"Failed to fetch source M3U. Status code: {response.status_code}")
