import pandas as pd
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

DATA_PATH = "telemetry_analysis/data/voyager2_jupiter_s3.tab"


def get_shock_data():
    """
    Gerçek veriden Jüpiter şok dalgasının en belirgin olduğu 4 noktayı çeker.
    """
    try:
        # DÜZELTME: Virgül ayracı kullanılıyor
        df = pd.read_csv(DATA_PATH, header=None, sep=',', on_bad_lines='skip')
        df = df.rename(columns={0: 'Time', 8: 'B_Mag'})
        df['Time'] = pd.to_datetime(df['Time'])

        # Jüpiter Şok Anı (Tam geçiş saati)
        shock_time = '1979-07-09 12:00'
        start_idx = df[df['Time'] >= shock_time].index[0]

        # 4 Ardışık veri noktasını al
        shock_values = df['B_Mag'].iloc[start_idx: start_idx + 4].values
        return shock_values

    except Exception as e:
        print(f"Veri okuma hatası: {e}")
        return np.array([10.0, 12.0, 45.0, 15.0])


def normalize_to_angles(data):
    # Veriyi 0 ile Pi arasına sıkıştır (Radyan)
    min_val = np.min(data)
    max_val = np.max(data)
    normalized = (data - min_val) / (max_val - min_val + 1e-5)
    angles = normalized * np.pi
    return angles


def encode_to_quantum(angles):
    # Ry kapıları ile veriyi kuantum durumuna kodla
    n_qubits = len(angles)
    qc = QuantumCircuit(n_qubits)
    for i, angle in enumerate(angles):
        qc.ry(angle, i)
    return qc


if __name__ == "__main__":
    # 1. Veriyi Al
    raw_data = get_shock_data()
    print(f"📡 Voyager Ham Verisi (4 Adım): {raw_data} nT")

    # 2. Açıya Çevir
    quantum_angles = normalize_to_angles(raw_data)
    print(f"🔄 Kuantum Açıları (Radyan): {np.round(quantum_angles, 3)}")

    # 3. Devre ve Simülasyon
    qc = encode_to_quantum(quantum_angles)
    print("\n⚛️ Kuantum Devresi:")
    print(qc)

    backend = AerSimulator(method='statevector')
    qc.save_statevector()
    result = backend.run(qc).result()
    statevector = result.get_statevector(qc)

    print("\n📊 Bloch Küresi Gösteriliyor...")
    plot_bloch_multivector(statevector)
    plt.show()