import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity

DATA_PATH = "voyager2_jupiter_s3.tab"

def load_vector_data():
    """Voyager 2'nin 3 boyutlu (X, Y, Z) manyetik verisini çeker."""
    try:
        df = pd.read_csv(DATA_PATH, header=None, sep=',', on_bad_lines='skip')
        # Sütunlar: 3(Br), 4(Bt), 5(Bn) -> 3 Boyutlu Veri
        df = df.iloc[:, [0, 3, 4, 5]]
        df.columns = ['Time', 'Bx', 'By', 'Bz']
        df['Time'] = pd.to_datetime(df['Time'])

        # Jüpiter Şok Geçişi
        mask = (df['Time'] >= '1979-07-08 12:00') & (df['Time'] <= '1979-07-10 00:00')
        return df.loc[mask].reset_index(drop=True)
    except Exception as e:
        print(f"Hata: {e}")
        return None


def encode_multidimensional(data_row, min_vals, max_vals):
    """
    3 Farklı veriyi (Bx, By, Bz) alır ve
    3 Qubit'lik DOLANIK (Entangled) bir devreye kodlar.
    """
    qc = QuantumCircuit(3)

    # 1. ENCODING (Her veriyi kendi Qubit'ine yükle)
    for i, val in enumerate(data_row):  # i=0(Bx), 1(By), 2(Bz)
        # Normalize et (0 - Pi arası)
        norm_val = (val - min_vals[i]) / (max_vals[i] - min_vals[i] + 1e-6)
        angle = norm_val * np.pi
        qc.ry(angle, i)  # Her qubit'i kendi verisi kadar döndür

    # 2. ENTANGLEMENT (Veriler arası ilişkiyi kur)
    # Bu adım, "Karmaşıklığın" başladığı yerdir.
    # Qubit 0, Qubit 1'i etkiler; Qubit 1, Qubit 2'yi...
    qc.cx(0, 1)  # CNOT: Bx değişirse By de etkilensin
    qc.cx(1, 2)  # CNOT: By değişirse Bz de etkilensin
    qc.cx(2, 0)  # Ring connection (Halka bağlantı)

    return Statevector.from_instruction(qc)


def run_complex_analysis():
    print("🚀 3-Qubit Vektör Analizi Başlatılıyor...")
    df = load_vector_data()
    if df is None: return

    # Veriyi matris olarak al: [[x1, y1, z1], [x2, y2, z2]...]
    vectors = df[['Bx', 'By', 'Bz']].values

    # Her sütun için min/max bul (Normalizasyon için)
    min_vals = np.min(vectors, axis=0)
    max_vals = np.max(vectors, axis=0)

    print(f"📡 İşlenen Boyut: {vectors.shape} (Zaman x 3 Feature)")

    # 1. Referans Durumu (Sessiz Uzay Ortalaması)
    ref_vector = np.mean(vectors[:20], axis=0)
    state_ref = encode_multidimensional(ref_vector, min_vals, max_vals)

    # 2. Tarama
    fidelities = []
    for row in vectors:
        state_curr = encode_multidimensional(row, min_vals, max_vals)
        # 3 Qubit'lik uzayda (8 Boyutlu Hilbert Uzayı) benzerlik ölçümü
        fidelities.append(state_fidelity(state_ref, state_curr))

    anomaly_scores = 1 - np.array(fidelities)

    # 3. Görselleştirme
    plt.figure(figsize=(12, 6))
    plt.plot(df['Time'], anomaly_scores, color='#ff0055', label='3-Qubit Entangled Score')
    plt.title('Multi-Dimensional Quantum Anomaly Detection (Entangled)', color='white')
    plt.ylabel('Anomaly Score', color='white')
    plt.xlabel('Time', color='white')

    # Tema
    plt.gca().set_facecolor('#0b0c10')
    plt.gcf().set_facecolor('#1f2833')
    plt.tick_params(colors='white')
    plt.grid(alpha=0.2)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    run_complex_analysis()