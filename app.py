import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import GroverOperator, QFT
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Algorithm Lab", layout="wide")

st.title("⚛️ Quantum Algorithm Exploratory")
st.write("Bu araç, karmaşık kuantum algoritmalarının nasıl çalıştığını anlamak için tasarlanmıştır.")

# Algoritma Seçimi
algo = st.sidebar.selectbox("Algoritma Seçin", ["Temel Kapılar", "Grover Algoritması", "Shor (QFT Temelli)"])

if algo == "Grover Algoritması":
    st.header("🔍 Grover Algoritması")
    st.write("Veritabanı arama problemlerinde klasik algoritmalara göre karesel hızlanma sağlar.")

    # Basit bir 2-qubit Grover devresi (Hedef: '11' durumu)
    n_qubits = 2
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))  # Süperpozisyon

    # Oracle (Hedefi işaretleme: 11)
    qc.cz(0, 1)

    # Diffuser (Yansıtma)
    qc.h(range(n_qubits))
    qc.z(range(n_qubits))
    qc.cz(0, 1)
    qc.h(range(n_qubits))

    st.subheader("Grover Devre Şeması")
    st.pyplot(qc.draw(output='mpl'))


elif algo == "Shor (QFT Temelli)":
    st.header("🔑 Shor Algoritması & QFT")
    st.write("Shor algoritmasının kalbi olan Kuantum Fourier Dönüşümü (QFT), periyot bulma işlemini yapar.")

    n_qubits = st.slider("Qubit Sayısı (QFT Hassasiyeti)", 2, 5, 3)
    qc = QFT(num_qubits=n_qubits).decompose()

    st.subheader(f"{n_qubits} Qubitlik QFT Devresi")
    st.pyplot(qc.draw(output='mpl'))


else:
    st.info("Lütfen soldaki menüden bir algoritma seçerek simülasyonu başlatın.")

# Ortak Simülasyon Motoru
if st.button("Simülasyonu Çalıştır"):
    backend = AerSimulator()
    qc.measure_all()
    result = backend.run(qc).result()
    counts = result.get_counts()

    st.subheader("Simülasyon Çıktısı (Olasılıklar)")
    st.pyplot(plot_histogram(counts))