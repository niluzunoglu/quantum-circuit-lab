import os
import requests

# NASA PDS-PPI Node (UCLA) - Kesinleşmiş URL
# Dataset: Voyager 2 Jupiter Encounter Magnetometer Data (System III Coords)
# Dosya Adı: S3_48S.TAB (System 3 Coordinates, 48 Second Averages)
REAL_DATA_URL = "https://pds-ppi.igpp.ucla.edu/data/VG2-J-MAG-4-SUMM-S3COORDS-48.0SEC-V1.1/DATA/S3_48S.TAB"
SAVE_PATH = "telemetry_analysis/data/voyager2_jupiter_s3.tab"


def download_confirmed_data():
    print(f"📡 NASA UCLA Sunucusuna Bağlanılıyor...")
    print(f"🔗 Hedef: {REAL_DATA_URL}")

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Science-Bot)'}
        response = requests.get(REAL_DATA_URL, headers=headers, stream=True)

        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            print(f"✅ Dosya bulundu! İndiriliyor... (Tahmini boyut: ~15-20 MB)")

            with open(SAVE_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"💾 Kaydedildi: {SAVE_PATH}")
        else:
            print(f"❌ Hata! Sunucu yanıtı: {response.status_code}")
            print("Link yapısı değişmiş olabilir, lütfen tarayıcıdan kontrol edin.")

    except Exception as e:
        print(f"⚠️ Bağlantı hatası: {e}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    download_confirmed_data()