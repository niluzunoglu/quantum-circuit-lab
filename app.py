import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Circuit Lab", layout="wide")

st.title("Quantum Circuit Lab")
st.write("Bu proje, kuantum hesaplama temellerini görselleştirmek için geliştirilmiştir.")

st.sidebar.header("Devre Ayarları")
n_qubits = st.sidebar.slider("Qubit Sayısı", 1, 3, 1)
gate_selection = st.sidebar.multiselect(
    "Uygulanacak Kapılar",
    ["Hadamard (H)", "Pauli-X (NOT)", "CNOT"],
    default=["Hadamard (H)"]
)

qc = QuantumCircuit(n_qubits)

if "Hadamard (H)" in gate_selection:
    qc.h(0)
if "Pauli-X (NOT)" in gate_selection:
    qc.x(0)
if "CNOT" in gate_selection and n_qubits > 1:
    qc.cx(0, 1)

st.subheader("1. Kuantum Devre Şeması")
fig_circuit = qc.draw(output='mpl')
st.pyplot(fig_circuit)

st.subheader("2. Simülasyon Sonuçları")
backend = AerSimulator()
qc.measure_all()
job = backend.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

col1, col2 = st.columns(2)
with col1:
    st.write("Olasılık Dağılımı")
    st.pyplot(plot_histogram(counts))

with col2:
    st.info("Bu bölümde qubitlerin süperpozisyon ve dolanıklık durumları simüle edilir.")

with st.expander("📖 Kuantum Kapıları Hakkında Bilgi"):
    st.markdown("""
    - **Hadamard (H):** Qubiti süperpozisyon durumuna sokar.
    - **Pauli-X:** Klasik bilgisayardaki NOT kapısının karşılığıdır.
    - **CNOT:** İki qubit arasında dolanıklık (entanglement) oluşturur.
    """)