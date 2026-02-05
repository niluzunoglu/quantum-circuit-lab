import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/voyager2_jupiter_s3.tab"


def load_and_visualize():
    print(f"📂 Dosya analiz ediliyor: {DATA_PATH}")

    try:
        df = pd.read_csv(DATA_PATH, header=None, sep=',', on_bad_lines='skip')

        # 0: Time
        # 5, 6, 7: Bx, By, Bz (Bileşenler)
        # 8: B_Magnitude (Alan Şiddeti - Aradığımız veri)
        df = df.rename(columns={0: 'Time', 8: 'B_Mag'})

        # Zaman formatını düzelt
        df['Time'] = pd.to_datetime(df['Time'])

        # Jüpiter Geçiş Anı (9 Temmuz 1979)
        start_date = '1979-07-08'
        end_date = '1979-07-10'

        mask = (df['Time'] >= start_date) & (df['Time'] <= end_date)
        df_zoom = df.loc[mask]

        print(f"📊 Toplam Veri: {len(df)} satır")
        print(f"🚀 Jüpiter Yakın Geçiş Verisi: {len(df_zoom)} satır")

        # Çizim
        plt.figure(figsize=(12, 6))
        plt.plot(df_zoom['Time'], df_zoom['B_Mag'], color='#00ffcc', linewidth=1.5, label='Magnetic Magnitude')

        plt.title('Voyager 2: Jupiter Bow Shock Crossing (Real Data)', fontsize=14, color='white')
        plt.xlabel('Date (July 1979)', fontsize=12, color='white')
        plt.ylabel('Magnetic Field (nT)', fontsize=12, color='white')

        # Tema
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.gca().set_facecolor('#0b0c10')
        plt.gcf().set_facecolor('#1f2833')
        plt.tick_params(colors='white')
        plt.legend()
        plt.tight_layout()

        plt.show()

    except Exception as e:
        print(f"⚠️ Hata: {e}")


if __name__ == "__main__":
    load_and_visualize()