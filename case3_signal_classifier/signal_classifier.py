import sys
import os
import matplotlib
matplotlib.use('Agg') # Save plots to file without opening window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

# Qiskit 1.0+ Modern Primitives
from qiskit.primitives import StatevectorSampler
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit_machine_learning.neural_networks import SamplerQNN
from qiskit_algorithms.utils import algorithm_globals

# Optimization via SciPy (Removing intermediaries)
from scipy.optimize import minimize

import warnings
warnings.filterwarnings('ignore')

# PATH CONFIGURATION
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
DATA_PATH = os.path.join(project_root, 'data', 'voyager2_jupiter_s3.tab')

# --- 1. DATASET CREATION ---
def create_dataset():
    print(f"🔍 Data Path: {DATA_PATH}")
    print("📡 Preparing Signal Dataset...")
    
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH, header=None, sep=',', on_bad_lines='skip')
            raw_data = df.iloc[5000:5400, 8].values 
            raw_data = raw_data[~np.isnan(raw_data)]
            print("✅ Real Voyager data loaded successfully.")
        else:
            raise FileNotFoundError("File not found")
    except Exception:
        print("⚠️ WARNING: Data not found, generating synthetic dataset.")
        raw_data = np.random.normal(10, 2, 400)

    # Reshape for 4-Qubit input
    X_natural = raw_data[:len(raw_data)//4 * 4].reshape(-1, 4)
    y_natural = np.zeros(len(X_natural))

    # Generate Artificial Signal (Sine Wave)
    t = np.linspace(0, 20, len(raw_data))
    artificial_wave = 5 * np.sin(t) + 10 + np.random.normal(0, 0.5, len(raw_data))
    X_artificial = artificial_wave[:len(artificial_wave)//4 * 4].reshape(-1, 4)
    
    # Balance classes
    min_len = min(len(X_natural), len(X_artificial))
    X_artificial = X_artificial[:min_len]
    X_natural = X_natural[:min_len]
    y_artificial = np.ones(min_len)

    # Concatenate
    X = np.concatenate([X_natural, X_artificial])
    y = np.concatenate([y_natural[:min_len], y_artificial])

    # Normalize (0 to 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y

# --- HELPER: PARITY FUNCTION ---
def parity(x):
    return "{:b}".format(x).count("1") % 2

# --- 2. MANUAL TRAINING LOOP ---
def train_model():
    X, y = create_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    print(f"📊 Training Set: {len(X_train)} samples")
    print(f"🧪 Test Set:     {len(X_test)} samples")

    # --- QUANTUM CIRCUIT ---
    num_inputs = 4
    feature_map = ZZFeatureMap(num_inputs)
    ansatz = RealAmplitudes(num_inputs, reps=2)
    
    qc = QuantumCircuit(num_inputs)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)
    
    # --- QNN CONSTRUCTION ---
    print("🧠 Building Quantum Neural Network (SamplerQNN)...")
    
    qnn = SamplerQNN(
        circuit=qc,
        input_params=feature_map.parameters,
        weight_params=ansatz.parameters,
        interpret=parity,
        output_shape=2,
        sampler=StatevectorSampler()
    )
    
    # --- COST FUNCTION ---
    loss_history = []
    
    def cost_func(params_values):
        # Forward pass
        probs = qnn.forward(X_train, params_values)
        
        # Calculate MSE Loss
        # We focus on the probability of class 1
        cost = np.sum((probs[:, 1] - y_train) ** 2) / len(y_train)
        
        loss_history.append(cost)
        print(f"📉 Step {len(loss_history)} | Loss: {cost:.4f}", end='\r')
        return cost

    # --- INITIALIZATION ---
    initial_weights = 0.1 * (2 * algorithm_globals.random.random(qnn.num_weights) - 1)
    
    print("\n🚀 Starting Manual Optimization (COBYLA)...")
    start_time = time.time()
    
    # Direct SciPy Optimization
    result = minimize(
        cost_func, 
        initial_weights, 
        method='COBYLA', 
        options={'maxiter': 150}
    )
    
    end_time = time.time()
    print(f"\n✅ Training Completed! Duration: {end_time - start_time:.2f}s")
    
    optimal_weights = result.x

    # --- TESTING PHASE ---
    print("🔍 Evaluating Model on Test Data...")
    test_probs = qnn.forward(X_test, optimal_weights)
    y_pred = np.where(test_probs[:, 1] > 0.5, 1, 0)
    
    test_acc = accuracy_score(y_test, y_pred)
    print(f"\n🏆 Test Accuracy: {test_acc * 100:.2f}%")

    # --- VISUALIZATION ---
    print("📈 Generating Plots...")
    plt.figure(figsize=(12, 6))

    # Plot 1: Loss
    plt.subplot(1, 2, 1)
    plt.plot(loss_history, color='#00ffcc', linewidth=2, label='Training Loss')
    plt.title('Training Convergence (MSE Loss)')
    plt.xlabel('Iterations')
    plt.ylabel('Loss Value')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.gca().set_facecolor('#0b0c10')

    # Plot 2: Predictions
    plt.subplot(1, 2, 2)
    
    subset_test = X_test[:20]
    subset_y = y_test[:20]
    subset_pred = y_pred[:20]
    
    plt.scatter(range(20), subset_y, c='gray', s=100, alpha=0.5, label='Ground Truth')
    plt.scatter(range(20), subset_pred, c='#ff0055', marker='x', s=100, label='Quantum Prediction')
    plt.title('Prediction Performance (First 20 Samples)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().set_facecolor('#0b0c10')

    plt.tight_layout()
    
    # SAVE TO FILE
    save_path = os.path.join(current_dir, 'case2_manual_loss.png')
    plt.savefig(save_path)
    print(f"\n✅ Graph saved successfully: {save_path}")
    print("👉 Please check 'case2_manual_loss.png' in the folder.")

if __name__ == "__main__":
    train_model()