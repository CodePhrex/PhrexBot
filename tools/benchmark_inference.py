"""Explicit operator benchmark; never reads project evidence or credentials."""
import argparse
import json
import time
import requests

PROMPT = "In one sentence, explain why a fictional library labels its books."

def benchmark(model):
    started = time.monotonic()
    first = None
    final = None
    with requests.post("http://127.0.0.1:11434/api/chat", json={
        "model": model, "messages": [{"role": "user", "content": PROMPT}],
        "stream": True, "options": {"num_predict": 64}
    }, stream=True, timeout=(5, 180)) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            frame = json.loads(line)
            if frame.get("error"):
                raise RuntimeError("Inference benchmark failed")
            if first is None and frame.get("message", {}).get("content"):
                first = time.monotonic() - started
            if frame.get("done"):
                final = frame
                break
    if final is None or first is None:
        raise RuntimeError("Incomplete benchmark")
    return {"model": model, "first_token_seconds": round(first, 3),
            "total_seconds": round(time.monotonic()-started, 3),
            "generated_tokens": final.get("eval_count"),
            "provider_generation_ns": final.get("eval_duration")}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", nargs="+")
    parser.add_argument("--allow-cloud", action="store_true")
    args = parser.parse_args()
    for model in args.model:
        if model.endswith(":cloud") and not args.allow_cloud:
            parser.error("Cloud benchmark requires explicit --allow-cloud")
        print(json.dumps(benchmark(model)))
