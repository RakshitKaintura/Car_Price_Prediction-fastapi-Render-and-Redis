import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()

# Use the environment variable provided by Render or local .env
REDIS_URL = os.getenv("REDIS_URL")

# Initialize client with decode_responses=True for easy string handling
redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

def get_cached_prediction(key: str):
    value = redis_client.get(key)
    # Use json.loads instead of eval for safety and performance
    return json.loads(value) if value else None

def set_cached_prediction(key: str, value: dict, expire_seconds: int = 3600):
    # Use json.dumps to store as a valid JSON string
    # Added an expiration (1 hour) to keep the cache fresh
    redis_client.set(key, json.dumps(value), ex=expire_seconds)