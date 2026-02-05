import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity

# Veri Yolu
DATA_PATH = "data/voyager2_jupiter_s3.tab"


def load_data():
    """Veriyi yükler ve Jüpiter geçişine odaklar."""
    try:
        df = pd.read_csv(DATA_PATH, header=None, sep=',', on_bad_lines='skip')
        df = df.rename(columns={0: 'Time', 8: 'B_Mag'})
        df['Time'] = pd.to_datetime(df['Time'])

        # Jüpiter Şok Geçişi (Zoom) - Temmuz 1979 başı
        # Analiz hızlı olsun diye sadece 300 veri noktasını alıyoruz
        mask = (df['Time'] >= '1979-07-08 00:00') & (df['Time'] <= '1979-07-10 00:00')
        return df.loc[mask].reset_index(drop=True)
    except Exception as e:
        print(f"Hata: {e}")
        return None


def data_to_quantum_state(value, min_val, max_val):
    """
    Tek bir sayısal değeri (Magnetic Field) Kuantum Durumuna (Statevector) çevirir.
    Yöntem: Ry Rotation (Y ekseninde döndürme)
    """
    # 1. Veriyi 0 ile Pi arasına normalize et
    norm_val = (value - min_val) / (max_val - min_val + 1e-6)
    angle = norm_val * np.pi

    # 2. Kuantum Devresi Kur (1 Qubit)
    qc = QuantumCircuit(1)
    qc.ry(angle, 0)  # Qubit'i 'angle' kadar döndür

    # 3. Durum Vektörünü (Statevector) Hesapla
    return Statevector.from_instruction(qc)


def run_anomaly_detection():
    print("🚀 Kuantum Anomali Dedektörü Başlatılıyor...")

    # 1. Veriyi Yükle
    df = load_data()
    if df is None: return

    magnetic_data = df['B_Mag'].values
    min_val, max_val = np.min(magnetic_data), np.max(magnetic_data)

    print(f"📊 Analiz Edilen Veri Noktası: {len(magnetic_data)}")

    # 2. REFERANS DURUMU BELİRLE (Sessiz Uzay)
    # İlk 10 verinin ortalamasını 'Normal Uzay' kabul ediyoruz.
    reference_value = np.mean(magnetic_data[:10])
    reference_state = data_to_quantum_state(reference_value, min_val, max_val)

    print(f"🌌 Referans (Normal) Değer: {reference_value:.2f} nT")

    # 3. TARAMA (Scanning)
    # Her veri noktası için 'Fidelity' hesapla
    fidelities = []

    for value in magnetic_data:
        # Mevcut veriyi kuantum durumuna çevir
        current_state = data_to_quantum_state(value, min_val, max_val)

        # Referans ile benzerliğini ölç (0 ile 1 arası)
        # 1.0 = Birebir Aynı, 0.0 = Tamamen Zıt
        fid = state_fidelity(reference_state, current_state)
        fidelities.append(fid)

    # 4. ANOMALİ SKORU (Ters Fidelity)
    # Benzerlik ne kadar düşükse, anomali o kadar yüksektir.
    anomaly_scores = 1 - np.array(fidelities)

    # 5. GÖRSELLEŞTİRME
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Sol Eksen: Gerçek Manyetik Alan
    color = 'tab:cyan'
    ax1.set_xlabel('Zaman (Örnekler)')
    ax1.set_ylabel('Manyetik Alan (nT)', color=color)
    ax1.plot(magnetic_data, color=color, label='Voyager 2 Signal')
    ax1.tick_params(axis='y', labelcolor=color)

    # Sağ Eksen: Kuantum Anomali Skoru
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Quantum Anomaly Score (0-1)', color=color)
    ax2.plot(anomaly_scores, color=color, linestyle='--', label='Anomaly Score')
    ax2.tick_params(axis='y', labelcolor=color)

    # Threshold Çizgisi (Örn: 0.1 üzeri anomali)
    plt.axhline(y=0.1, color='white', linestyle=':', alpha=0.5, label='Threshold')

    plt.title('Quantum Anomaly Detection: Jupiter Bow Shock')

    # Koyu Tema Ayarları
    fig.patch.set_facecolor('#1e1e1e')
    ax1.set_facecolor('#0b0c10')
    ax1.xaxis.label.set_color('white')
    ax1.yaxis.label.set_color('white')
    ax2.yaxis.label.set_color('white')
    ax1.title.set_color('white')
    ax1.tick_params(colors='white')
    ax2.tick_params(colors='white')

    plt.show()


if __name__ == "__main__":
    run_anomaly_detection()