import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import QFT
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quantum Lab",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True) # Hatalı kısım burasıydı, düzelttim.

st.title("Quantum Computing Research Laboratory")
st.markdown("---")

with st.sidebar:
    st.header("Control Panel")
    algo = st.selectbox(
        "Select Algorithm",
        ["Basic Gates", "Grover's Search", "Quantum Fourier Transform"]
    )

    st.markdown("---")
    st.info("This environment uses the Qiskit Aer high-performance simulator for circuit execution.")

qc = None

if algo == "Basic Gates":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Configuration")
        gate_type = st.radio("Gate Type", ["Hadamard", "Pauli-X", "Pauli-Z"])
        qc = QuantumCircuit(1)
        if gate_type == "Hadamard":
            qc.h(0)
        elif gate_type == "Pauli-X":
            qc.x(0)
        else:
            qc.z(0)

    with col2:
        st.subheader("Circuit Architecture")
        st.pyplot(qc.draw(output='mpl'))

elif algo == "Grover's Search":
    st.subheader("Grover's Algorithm (2-Qubit State Search)")

    tab1, tab2 = st.tabs(["Mathematical Logic", "Circuit Visualization"])

    with tab1:
        st.latex(r"G = (2|\psi\rangle\langle\psi| - I) O")
        st.markdown(
            "The algorithm enhances the probability amplitude of the target state through reflection about the average.")

    with tab2:
        qc = QuantumCircuit(2)
        qc.h(range(2))
        qc.cz(0, 1)
        qc.h(range(2))
        qc.z(range(2))
        qc.cz(0, 1)
        qc.h(range(2))
        st.pyplot(qc.draw(output='mpl'))

elif algo == "Quantum Fourier Transform":
    st.subheader("Quantum Fourier Transform (QFT)")
    n_qubits = st.slider("Qubit Register Size", 2, 6, 3)

    with st.expander("Theoretical Foundation"):
        st.latex(r"QFT_N |j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} \omega_N^{jk} |k\rangle")

    qc = QFT(num_qubits=n_qubits).decompose()
    st.pyplot(qc.draw(output='mpl'))

st.markdown("---")

if qc:
    if st.button("Execute Quantum Simulation"):
        with st.spinner("Processing quantum states..."):
            backend = AerSimulator()
            m_qc = qc.copy()
            m_qc.measure_all()

            result = backend.run(m_qc, shots=2048).result()
            counts = result.get_counts()

            res_col1, res_col2 = st.columns([2, 1])
            with res_col1:
                st.subheader("Probability Distribution")
                st.pyplot(plot_histogram(counts))

            with res_col2:
                st.subheader("Measurement Data")
                st.write(counts)