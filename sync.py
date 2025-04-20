import requests

source_url = "https://raw.githubusercontent.com/DRAG-10/DRAG10/refs/heads/special/DRAG10.m3u"
target_path = "dragon.m3u"

response = requests.get(source_url)

if response.status_code == 200:
    lines = response.text.splitlines()

    
    unwanted_lines = [
        "LİSTE @DRAG10 TARAFINDAN YAPILMIŞTIR",
        "ORTAK @SYNDRAXİC",
        source_url,
        "#EXTM3U"
    ]

   
    filtered_lines = [line for line in lines if line.strip() not in unwanted_lines]

    if filtered_lines and not filtered_lines[0].startswith("#EXTM3U"):
        filtered_lines.insert(0, "#EXTM3U")

    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered_lines))

else:
    print(f"Kaynak M3U alınamadı. Status code: {response.status_code}")
