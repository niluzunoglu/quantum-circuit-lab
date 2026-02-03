import pandas as pd
import matplotlib.pyplot as plt

# Dosya yolu
DATA_PATH = "telemetry_analysis/data/voyager2_magnetic_1979.asc"


def load_and_visualize():
    # Sütun İsimleri (NASA dökümantasyonuna göre)
    # Col 1: Spacecraft ID, Col 2: Coord Sys, Col 3: Year, Col 4: Day, Col 5: Hour, Col 6: Magnetic Field (B) Magnitude
    column_names = ["sc_id", "coord_sys", "year", "day", "hour", "B_mag", "B_avg", "elevation", "azimuth"]

    # Veriyi Oku (Boşluklarla ayrılmış veri)
    try:
        df = pd.read_csv(DATA_PATH, delim_whitespace=True, names=column_names, header=None)

        # Sadece Jüpiter'e yaklaştığı (örneğin 180. gün civarı) bir kesiti alalım
        # Çok büyük veriyi çizdirmemek için ilk 1000 örneği alıyoruz
        signal_slice = df['B_mag'].iloc[5000:6000]

        print(f"📊 Veri Yüklendi. Toplam Satır: {len(df)}")
        print(df.head())

        # Görselleştirme
        plt.figure(figsize=(12, 6))
        plt.plot(signal_slice.values, label='Voyager 2 - Magnetic Field (nT)', color='cyan', linewidth=0.8)
        plt.title('Voyager 2 Deep Space Telemetry (Jupiter Flyby - 1979)')
        plt.xlabel('Time (48s intervals)')
        plt.ylabel('Magnetic Field Magnitude (nT)')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)

        plt.gca().set_facecolor('black')
        plt.gcf().set_facecolor('#1e1e1e')
        plt.tick_params(colors='white')
        plt.title('Voyager 2 Telemetry', color='white')
        plt.ylabel('Magnitude', color='white')
        plt.xlabel('Samples', color='white')

        plt.show()

    except FileNotFoundError:
        print("❌ Dosya bulunamadı! Önce 'fetch_data.py' dosyasını çalıştırın.")


if __name__ == "__main__":
    load_and_visualize()