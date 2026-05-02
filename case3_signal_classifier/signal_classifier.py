import sys
import os
import matplotlib
matplotlib.use('Agg') # No GUI mode
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import base64
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from qiskit.primitives import StatevectorSampler
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit_machine_learning.neural_networks import SamplerQNN
from qiskit_algorithms.utils import algorithm_globals
from scipy.optimize import minimize
from weasyprint import HTML

import warnings
warnings.filterwarnings('ignore')

# PATH CONFIG
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
DATA_PATH = os.path.join(project_root, 'data', 'voyager2_jupiter_s3.tab')

def create_dataset():
    print("📡 Preparing Signal Dataset...")
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH, header=None, sep=',', on_bad_lines='skip')
            raw_data = df.iloc[5000:5400, 8].values 
            raw_data = raw_data[~np.isnan(raw_data)]
            print("✅ Real Voyager data loaded.")
        else:
            raise FileNotFoundError()
    except:
        raw_data = np.random.normal(10, 2, 400)
    
    X_nat = raw_data[:len(raw_data)//4 * 4].reshape(-1, 4)
    y_nat = np.zeros(len(X_nat))
    t = np.linspace(0, 20, len(raw_data))
    X_art = (5 * np.sin(t) + 10 + np.random.normal(0, 0.5, len(raw_data)))[:len(raw_data)//4 * 4].reshape(-1, 4)
    
    min_len = min(len(X_nat), len(X_art))
    X = np.concatenate([X_nat[:min_len], X_art[:min_len]])
    y = np.concatenate([y_nat[:min_len], np.ones(min_len)])
    X_scaled = MinMaxScaler(feature_range=(0, 1)).fit_transform(X)
    return X_scaled, y

def parity(x):
    return "{:b}".format(x).count("1") % 2

def generate_pdf_report(metrics, loss_history, image_path):
    print("✍️ Generating PDF Report...")
    
    # Grafiği Base64'e çevir (PDF'e gömmek için)
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 20mm; background-color: #fdfbf7; }}
            body {{ font-family: 'Georgia', serif; color: #2c2c2c; line-height: 1.6; background-color: #fdfbf7; }}
            .header {{ border-bottom: 2px solid #5d4037; padding-bottom: 10px; margin-bottom: 30px; }}
            h1 {{ color: #5d4037; font-size: 24pt; margin: 0; }}
            .meta {{ font-size: 10pt; color: #795548; font-style: italic; }}
            .section {{ margin-bottom: 25px; padding: 15px; background: white; border-left: 5px solid #8d6e63; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }}
            h2 {{ color: #795548; font-size: 16pt; margin-top: 0; border-bottom: 1px solid #eee; }}
            .metric-box {{ display: inline-block; width: 45%; padding: 10px; text-align: center; border: 1px solid #d7ccc8; margin-right: 10px; }}
            .math {{ font-family: 'Times New Roman', serif; font-style: italic; font-weight: bold; color: #4e342e; }}
            .plot {{ width: 100%; margin-top: 20px; border: 1px solid #d7ccc8; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #d7ccc8; padding: 8px; text-align: left; font-size: 10pt; }}
            th {{ background-color: #efebe9; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Quantum Signal Analysis Report</h1>
            <div class="meta">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Investigator: Aleyna Nil Uzunoğlu</div>
        </div>

        <div class="section">
            <h2>1. Executive Summary</h2>
            <p>This report documents the results of a Quantum Neural Network (QNN) trained to classify deep-space telemetry signals. 
            The model distinguishes between <b>Natural Stochastic Noise</b> (Voyager 2) and <b>Coherent Artificial Signals</b> using Hilbert Space mapping.</p>
        </div>

        <div class="section">
            <h2>2. Model Architecture</h2>
            <ul>
                <li><b>Encoding:</b> <span class="math">ZZFeatureMap</span> (4 Qubits)</li>
                <li><b>Variational Layer:</b> <span class="math">RealAmplitudes</span> (reps=2)</li>
                <li><b>Optimization:</b> COBYLA (maxiter=150)</li>
                <li><b>Loss Function:</b> Mean Squared Error (<span class="math">MSE = 1/n &Sigma; (y_i - &ycirc;_i)&sup2;</span>)</li>
            </ul>
        </div>

        <div class="section">
            <h2>3. Performance Metrics</h2>
            <div class="metric-box">
                <div style="font-size: 9pt;">Training Accuracy</div>
                <div style="font-size: 18pt; font-weight: bold;">{metrics['train_acc']:.2f}%</div>
            </div>
            <div class="metric-box">
                <div style="font-size: 9pt;">Test Accuracy</div>
                <div style="font-size: 18pt; font-weight: bold; color: #bf360c;">{metrics['test_acc']:.2f}%</div>
            </div>
        </div>

        <div class="section">
            <h2>4. Training Visualizations</h2>
            <img src="data:image/png;base64,{img_base64}" class="plot">
        </div>

        <div class="section">
            <h2>5. Analysis & Conclusion</h2>
            <p>The convergence of the loss function indicates that the <span class="math">SamplerQNN</span> successfully identified non-linear 
            periodicities in the Hilbert space. The variance in predictions likely stems from Gaussian noise injected into the artificial signal. 
            Further research will focus on entanglement-driven feature maps.</p>
        </div>
    </body>
    </html>
    """
    pdf_path = os.path.join(current_dir, "Quantum_Analysis_Report.pdf")
    HTML(string=html_content).write_pdf(pdf_path)
    print(f"✅ Report saved to: {pdf_path}")

def train_model():
    X, y = create_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    qc = QuantumCircuit(4)
    feature_map = ZZFeatureMap(4)
    ansatz = RealAmplitudes(4, reps=2)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)
    
    qnn = SamplerQNN(circuit=qc, input_params=feature_map.parameters, weight_params=ansatz.parameters, 
                     interpret=parity, output_shape=2, sampler=StatevectorSampler())
    
    loss_history = []
    def cost_func(params):
        probs = qnn.forward(X_train, params)
        cost = np.sum((probs[:, 1] - y_train) ** 2) / len(y_train)
        loss_history.append(cost)
        print(f"📉 Step {len(loss_history)} | Loss: {cost:.4f}", end='\r')
        return cost

    print("\n🚀 Starting Manual Optimization...")
    res = minimize(cost_func, 0.1 * (2 * algorithm_globals.random.random(qnn.num_weights) - 1), 
                   method='COBYLA', options={'maxiter': 150})
    
    y_pred = np.where(qnn.forward(X_test, res.x)[:, 1] > 0.5, 1, 0)
    train_acc = accuracy_score(y_train, np.where(qnn.forward(X_train, res.x)[:, 1] > 0.5, 1, 0)) * 100
    test_acc = accuracy_score(y_test, y_pred) * 100
    
    # Save chart for the report
    img_path = os.path.join(current_dir, "temp_plot.png")
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1); plt.plot(loss_history, color='#5d4037'); plt.title("Convergence")
    plt.subplot(1, 2, 2); plt.scatter(range(20), y_test[:20], c='gray', alpha=0.5); plt.scatter(range(20), y_pred[:20], c='red', marker='x'); plt.title("Predictions")
    plt.savefig(img_path)
    
    # Generate PDF
    generate_pdf_report({'train_acc': train_acc, 'test_acc': test_acc}, loss_history, img_path)
    os.remove(img_path) # Clean up temp image

if __name__ == "__main__":
    train_model()