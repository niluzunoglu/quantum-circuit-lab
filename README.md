# Quantum-Circuit-Lab: Quantum Computing Research Laboratory

## Description
Quantum-Circuit-Lab is a comprehensive Python-based quantum computing research platform built on the IBM Qiskit framework. This project combines fundamental quantum algorithms (Grover Search and Quantum Fourier Transform) with real-world applications including Voyager 2 telemetry analysis and quantum anomaly detection. The platform provides both a visual simulation environment via Streamlit and advanced data analysis capabilities.

## Project Structure

```
quantum-circuit-lab/
├── app.py                                    # Main Streamlit application
├── quantum_engine.py                         # Core quantum computing engine
├── requirements.txt                          # Project dependencies
├── tests/
│   └── test_circuits.py                      # Unit tests for quantum circuits
├── case1_voyager_telemetry_analysis/         # Space mission telemetry analysis
│   ├── 0_fetch_data.py                       # Data fetching pipeline
│   ├── 1_process_signal.py                   # Signal processing module
│   ├── 5_benchmark_study.py                  # Performance benchmarking
│   ├── quantum_anomaly.py                    # Quantum-based anomaly detection
│   ├── quantum_bridge.py                     # Bridge between telemetry and quantum
│   └── data/
│       └── voyager2_jupiter_s3.tab           # Voyager 2 Jupiter encounter data
└── case2_anomaly_detection/                  # Advanced anomaly detection
    ├── complex_quantum.py                    # Complex quantum operations
    └── voyager2_jupiter_s3.tab               # Reference dataset
```

## Key Features

### Core Quantum Algorithms
- **Grover's Search Algorithm**: Oracle and diffusion operators for quantum search
- **Quantum Fourier Transform (QFT)**: Period-finding implementation, foundation of Shor's algorithm
- **Quantum Simulation**: Local execution using AerSimulator for high-fidelity analysis

### Applications
- **Voyager Telemetry Analysis**: Signal processing and anomaly detection on space mission data
- **Quantum Anomaly Detection**: Detection of anomalies using quantum computing techniques
- **Interactive Visualization**: Real-time circuit drawing and statistical analysis via Streamlit

### Testing
- Comprehensive unit tests for quantum circuit operations
- Validation of quantum gate logic and probability distributions

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/niluzunoglu/quantum-circuit-lab.git
   cd quantum-circuit-lab
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the interactive application:
   ```bash
   streamlit run app.py
   ```

## Requirements
- Python 3.9+
- Qiskit (quantum algorithms and circuits)
- Qiskit-Aer (quantum simulator)
- Streamlit (web interface)
- Matplotlib (visualization)
- Pylatexenc (circuit rendering)

## Usage

### Running the Web Interface
```bash
streamlit run app.py
```
Access the application at `http://localhost:8501`

### Running Telemetry Analysis
```bash
python case1_voyager_telemetry_analysis/0_fetch_data.py
python case1_voyager_telemetry_analysis/1_process_signal.py
```

### Running Tests
```bash
pytest tests/
```

## Project Roadmap
- [ ] Integration with IBM Quantum Experience (real hardware execution)
- [ ] Implementation of BB84 Quantum Key Distribution Protocol
- [ ] Noise modeling and thermal relaxation simulation
- [ ] Advanced Bloch multivector and density matrix visualizations
- [ ] Extended telemetry dataset support
- [ ] Performance optimization for multi-qubit systems

## Theoretical Background
This project serves as both a functional quantum computing platform and an educational resource. The implementation includes mathematical foundations for quantum interference, entanglement, and phase kickback mechanisms. Each algorithm is accompanied by circuit visualizations and probability analysis to aid understanding.

## License
MIT License

## Author
niluzunoglu
