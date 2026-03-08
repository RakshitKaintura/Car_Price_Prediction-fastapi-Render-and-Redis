import joblib
import pandas as pd
import os # Added for path verification
from app.core.config import settings
from app.cache.redis_cache import set_cached_prediction, get_cached_prediction

# Ensure the model file exists before loading to prevent startup crashes
if not os.path.exists(settings.MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {settings.MODEL_PATH}")

# Load the model
model = joblib.load(settings.MODEL_PATH)

def predict_car_price(data: dict):
    # Create a unique cache key from input data
    cache_key = ":".join([str(val) for val in data.values()])
    
    # Check Redis cache first
    cached = get_cached_prediction(cache_key)
    if cached:
        return cached
    
    # Perform prediction if not in cache
    input_data = pd.DataFrame([data])
    prediction = model.predict(input_data)[0]
    
    # Store result in cache
    set_cached_prediction(cache_key, prediction)
    
    return prediction