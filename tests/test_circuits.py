import pytest
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def test_hadamard_logic():
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()

    backend = AerSimulator()
    result = backend.run(qc, shots=1000).result()
    counts = result.get_counts()

    assert '0' in counts
    assert '1' in counts
    assert 400 < counts['0'] < 600


def test_grover_oracle():
    qc = QuantumCircuit(2)
    qc.h(range(2))
    qc.cz(0, 1)
    qc.h(range(2))
    qc.z(range(2))
    qc.cz(0, 1)
    qc.h(range(2))
    qc.measure_all()

    backend = AerSimulator()
    result = backend.run(qc).result()
    counts = result.get_counts()

    max_state = max(counts, key=counts.get)
    assert max_state == '11'