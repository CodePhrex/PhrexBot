"""Read-only local Ollama readiness; no model downloads or process management."""
import requests

URL = 'http://127.0.0.1:11434/api/tags'

def readiness(model, session=None):
    if not isinstance(model, str) or not model.strip():
        return {'state': 'disabled', 'inference_ready': False}
    client = session or requests.Session()
    try:
        response = client.get(URL, timeout=(2, 3), allow_redirects=False)
        if response.status_code != 200:
            return {'state': 'unavailable', 'inference_ready': False}
        payload = response.json()
        models = payload.get('models') if isinstance(payload, dict) else None
        if not isinstance(models, list):
            return {'state': 'invalid_response', 'inference_ready': False}
        expected = model if ':' in model else model + ':latest'
        present = any(isinstance(item, dict) and item.get('name') == expected for item in models)
        return {'state': 'model_listed' if present else 'model_missing', 'inference_ready': False, 'model_listed': present}
    except (requests.RequestException, ValueError):
        return {'state': 'unavailable', 'inference_ready': False}
    finally:
        if session is None:
            client.close()
