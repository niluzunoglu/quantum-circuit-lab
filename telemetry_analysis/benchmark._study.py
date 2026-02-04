import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity

DATA_PATH = "telemetry_analysis/data/voyager2_jupiter_s3.tab"


# --- YARDIMCI FONKSİYONLAR ---
def load_data():
    df = pd.read_csv(DATA_PATH, header=None, sep=',', on_bad_lines='skip')
    df = df.rename(columns={0: 'Time', 8: 'B_Mag'})
    df['Time'] = pd.to_datetime(df['Time'])
    start_date = '1979-07-08 12:00'
    end_date = '1979-07-10 00:00'
    mask = (df['Time'] >= start_date) & (df['Time'] <= end_date)
    return df.loc[mask]['B_Mag'].values


def quantum_score(data):
    # Kuantum Fidelity Metodu
    min_val, max_val = np.min(data), np.max(data)
    scores = []

    # Referans (Sessiz Uzay)
    ref_val = np.mean(data[:20])
    qc_ref = QuantumCircuit(1)
    qc_ref.ry((ref_val - min_val) / (max_val - min_val) * np.pi, 0)
    state_ref = Statevector.from_instruction(qc_ref)

    for val in data:
        qc = QuantumCircuit(1)
        qc.ry((val - min_val) / (max_val - min_val) * np.pi, 0)
        state_curr = Statevector.from_instruction(qc)
        scores.append(1 - state_fidelity(state_ref, state_curr))  # Anomali Skoru
    return np.array(scores)


def classical_score(data):
    # Klasik Z-Score Metodu (Standart Sapma Bazlı)
    mean = np.mean(data[:20])  # Referans ortalama
    std = np.std(data[:20]) + 1e-6  # Referans sapma
    z_scores = np.abs((data - mean) / std)

    # 0-1 arasına normalize et (Karşılaştırma adil olsun diye)
    return z_scores / np.max(z_scores)


# --- DENEY ---
def run_benchmark():
    raw_signal = load_data()

    # Gürültü Seviyeleri (Noise Levels)
    noise_levels = [0, 5, 10]  # nT cinsinden eklenen rastgele gürültü

    fig, axes = plt.subplots(len(noise_levels), 1, figsize=(10, 12), sharex=True)

    for i, noise_amp in enumerate(noise_levels):
        # Sinyale Gürültü Ekle
        noisy_signal = raw_signal + np.random.normal(0, noise_amp, len(raw_signal))

        # Skorları Hesapla
        q_scores = quantum_score(noisy_signal)
        c_scores = classical_score(noisy_signal)

        # Çizdir
        ax = axes[i]
        ax.plot(q_scores, label='Quantum (Fidelity)', color='red', linewidth=1.5)
        ax.plot(c_scores, label='Classical (Z-Score)', color='blue', linestyle='--', alpha=0.7)
        ax.set_title(f'Noise Level: {noise_amp} nT', color='white')
        ax.legend()
        ax.grid(True, alpha=0.2)
        ax.set_facecolor('#0b0c10')
        ax.tick_params(colors='white')

    fig.patch.set_facecolor('#1e1e1e')
    plt.xlabel('Time Steps', color='white')
    plt.show()


if __name__ == "__main__":
    run_benchmark()