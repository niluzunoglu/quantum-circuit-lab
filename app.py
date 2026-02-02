import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import QFT
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Algorithm Lab", layout="wide")
st.title("Quantum Computing Algorithms Laboratory")
algo = st.sidebar.selectbox("Algoritma Seçin", ["Temel Kapılar (Hadamard)", "Grover Algoritması", "Shor (QFT)"])

qc = None

if algo == "Temel Kapılar (Hadamard)":
    st.header("Temel Kuantum Kapıları")
    qc = QuantumCircuit(1)
    qc.h(0)  # Sadece bir Hadamard kapısı
    st.write("Bu devre bir qubiti süperpozisyon durumuna sokar.")
    st.subheader("Devre Şeması")
    st.pyplot(qc.draw(output='mpl'))

elif algo == "Grover Algoritması":
    st.header("Grover Algoritması")
    with st.expander("Matematiksel Arka Plan"):
        st.latex(r"|\psi_{next}\rangle = (2|\psi\rangle\langle\psi| - I) U_\omega |\psi\rangle")

    qc = QuantumCircuit(2)
    qc.h(range(2))
    qc.cz(0, 1)  # Oracle
    qc.h(range(2))
    qc.z(range(2))
    qc.cz(0, 1)
    qc.h(range(2))

    st.subheader("Devre Şeması")
    st.pyplot(qc.draw(output='mpl'))

elif algo == "Shor (QFT)":
    st.header("Shor Algoritması ve QFT")
    n_qubits = st.slider("Qubit Sayısı", 2, 5, 3)
    qc = QFT(num_qubits=n_qubits).decompose()

    st.subheader(f"{n_qubits} Qubitlik QFT Devresi")
    st.pyplot(qc.draw(output='mpl'))

if qc is not None:
    if st.button("Simülasyonu Başlat"):
        backend = AerSimulator()
        measure_qc = qc.copy()
        measure_qc.measure_all()

        result = backend.run(measure_qc).result()
        counts = result.get_counts()

        st.subheader("Simülasyon Sonucu (Olasılıklar)")
        st.pyplot(plot_histogram(counts))
else:
    st.error("Devre oluşturulamadı.Lütfen bir algoritma seçin.")