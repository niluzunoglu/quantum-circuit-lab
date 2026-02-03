import os
import requests
import pandas as pd

# NASA SPDF Voyager 2 Manyetik Alan Verisi (48 saniye çözünürlüklü)
# 1979 Yılı - Jüpiter Geçişi (Sinyal aktivitesi yüksek)
DATA_URL = "https://spdf.gsfc.nasa.gov/pub/data/voyager/voyager2/magnetic_fields/ip_48s_ascii/data/vg2_48s_1979.asc"
SAVE_PATH = "telemetry_analysis/data/voyager2_magnetic_1979.asc"


def download_data():
    print(f"📡 NASA sunucularından veri çekiliyor: {DATA_URL}...")
    response = requests.get(DATA_URL)

    if response.status_code == 200:
        with open(SAVE_PATH, 'wb') as f:
            f.write(response.content)
        print(f"✅ Veri başarıyla kaydedildi: {SAVE_PATH}")
        print(f"Dosya Boyutu: {len(response.content) / 1024:.2f} KB")
    else:
        print(f"❌ Hata oluştu. Status Code: {response.status_code}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    download_data()