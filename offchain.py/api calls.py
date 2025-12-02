from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from typing import List

# --- Load Model and Data (Pre-loaded for fast API response) ---
MODEL_PATH = 'isolation_forest_model.joblib'
DB_PATH = 'transaction_database.csv'

try:
    # Load the previously trained model and the mock database
    # In a real system, the model would predict on LIVE, new data.
    model = joblib.load(MODEL_PATH)
    db = pd.read_csv(DB_PATH)
    print("API: Model and Database loaded successfully.")
except FileNotFoundError:
    print("ERROR: Run 'python train_model.py' first to generate files.")
    exit()

app = FastAPI(title="AI Fraud Score Service")

# --- Define API Endpoint ---

@app.post("/get-score")
def get_fraud_score(tx_id: str):
    """
    Fetches the pre-calculated fraud score for a given transaction ID.
    (In a real-time system, this would trigger the model to predict on new feature data.)
    """
    
    # 1. Look up the transaction in the mock database
    transaction = db[db['tx_id'] == tx_id]
    
    if transaction.empty:
        # In a live system, you would try to fetch the features and predict here.
        raise HTTPException(status_code=404, detail=f"Transaction ID {tx_id} not found.")

    # 2. Extract the pre-calculated score
    score = transaction['fraud_score'].iloc[0]
    
    # 3. Return the score
    return {
        "transaction_id": tx_id,
        "score": round(score), # Return as integer (0-100) for clean transfer to Solana (u8)
        "model_used": "IsolationForest"
    }

# To run this service, you would typically use uvicorn:
# uvicorn api_service:app --reload --port 8000
