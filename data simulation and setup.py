import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# --- 1. Generate Synthetic Data ---
def generate_transaction_data(n_samples=10000, n_fraud=100):
    rng = np.random.RandomState(42)
    
    # 9900 Normal Transactions (Group 1: Low values, high frequency)
    X_normal = 0.5 * rng.randn(n_samples - n_fraud, 3)
    X_normal[:, 0] += 5 # feature 1: average transaction value
    X_normal[:, 1] += 5 # feature 2: time since last transaction (low)
    X_normal[:, 2] += 2 # feature 3: geographic distance
    
    # 100 Fraud Transactions (Group 2: High values, low frequency, large distance)
    X_fraud = 0.5 * rng.randn(n_fraud, 3)
    X_fraud[:, 0] += 15 # High transaction value
    X_fraud[:, 1] += 15 # Long time since last similar transaction (suspicious)
    X_fraud[:, 2] += 10 # Large geographic distance
    
    X = np.concatenate([X_normal, X_fraud])
    
    # Create DataFrame and apply scaling
    df = pd.DataFrame(X, columns=['Amount', 'TimeSinceLast', 'GeoDistance'])
    
    # Standardize data for Isolation Forest
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    
    return pd.DataFrame(df_scaled, columns=df.columns), X # Return original data too for identification

# Generate the data
df_transactions, original_data = generate_transaction_data()
df_transactions['tx_id'] = [f"TX-{i:05d}" for i in range(len(df_transactions))]

print("Generated data sample (first 5 rows):")
print(df_transactions.head())

