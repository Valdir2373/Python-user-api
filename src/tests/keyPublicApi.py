import hashlib
from datetime import datetime

SECRET_KEY = "gmzinBBgemedor"


def GeneratePublicToken(path: str, method: str) -> dict:
    timestamp_ms = str(int(datetime.now().timestamp() * 1000))
    
    raw_payload = f"{SECRET_KEY}{timestamp_ms}{path}{method.upper()}"
    
    hash_result = hashlib.sha256(raw_payload.encode()).hexdigest()
    
    return {
        "x-gm-token": hash_result,
        "x-gm-timestamp": timestamp_ms
    }
