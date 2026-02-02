# Quantum-Circuit-Lab: Implementation of Grover and Shor/QFT

### Description
This repository contains a Python-based implementation of fundamental quantum algorithms using the IBM Qiskit framework. The project aims to demonstrate the practical application of quantum gate logic and provide a visual simulation environment for analyzing quantum state probability distributions. The implementation focuses on the Grover Search Algorithm for unstructured data and the Quantum Fourier Transform (QFT), which is the computational core of Shor's Factoring Algorithm.

### Technical Components
- Grover's Search Algorithm: Implementation of oracle and diffusion operators for 2-qubit systems.
- Quantum Fourier Transform (QFT): Scalable implementation of period-finding circuits.
- Simulation Engine: Local execution using AerSimulator for high-fidelity result analysis.
- Visualization: Integrated graphical user interface for real-time circuit drawing and histogram generation.

## Project Roadmap
- [ ] Integration with IBM Quantum Experience (Real Hardware Execution)
- [ ] Implementation of BB84 Quantum Key Distribution Protocol
- [ ] Support for Noise Modeling and Thermal Relaxation Simulation
- [ ] Advanced Visualizations (Bloch Multivectors and Density Matrices)
- [ ] Automated Unit Testing for Quantum Circuits using Qiskit Terra

### Installation and Usage
Follow the steps below to set up the local development environment:

1. Clone the repository:
   git clone https://github.com/niluzunoglu/quantum-circuit-lab.git

2. Install the required dependencies:
   pip install -r requirements.txt

3. Execute the simulation:
   streamlit run app.py

### Requirements
- Python 3.9+
- Qiskit
- Qiskit-Aer
- Streamlit
- Matplotlib
- Pylatexenc (for circuit visualization)

### Theoretical Background
The project includes mathematical derivations within the application interface to provide context for the gate operations. This hybrid approach serves both as a functional software tool and a pedagogical resource for understanding quantum interference and entanglement.
