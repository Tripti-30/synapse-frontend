import joblib
from sklearn.ensemble import IsolationForest
from data_prep import df_transactions

# --- 2. Train Isolation Forest Model ---

# Data to train on (excluding the tx_id)
X_train = df_transactions.drop(columns=['tx_id']) 

# Initialize the Isolation Forest model
# 'contamination' is the expected proportion of outliers in the dataset.
# Set it to 1% (100 fraud samples out of 10000 total)
model = IsolationForest(
    n_estimators=100, 
    contamination=0.01, 
    random_state=42
)

# Train the model
model.fit(X_train)

# Save the trained model to a file
MODEL_PATH = 'isolation_forest_model.joblib'
joblib.dump(model, MODEL_PATH)

print(f"\nIsolation Forest Model trained and saved to {MODEL_PATH}")

# --- 3. Test Prediction and Score Calculation ---

# Get the anomaly score (negative values are anomalies/fraud)
anomaly_scores = model.decision_function(X_train)

# Convert the anomaly score to a normalized Fraud Score (0 to 100)
# The more negative the score, the higher the risk (closer to 100).
# A common method is to use a sigmoid or min/max normalization.
# Simple normalization for presentation:
min_score = anomaly_scores.min()
max_score = anomaly_scores.max()
normalized_scores = 100 * (1 - (anomaly_scores - min_score) / (max_score - min_score))

df_transactions['anomaly_score'] = anomaly_scores
df_transactions['fraud_score'] = normalized_scores.round(2)

# Display the top 5 highest fraud scores (should be close to 100)
print("\nTop 5 Highest Risk Transactions:")
top_risks = df_transactions.sort_values(by='fraud_score', ascending=False).head(5)
print(top_risks[['tx_id', 'fraud_score', 'anomaly_score']])

# Example of a low risk score (should be close to 0)
print("\nExample Low Risk Score:")
low_risk = df_transactions.sort_values(by='fraud_score', ascending=True).head(5)
print(low_risk[['tx_id', 'fraud_score', 'anomaly_score']])

# You can now use this DataFrame as a mock database
df_transactions.to_csv('transaction_database.csv', index=False)

