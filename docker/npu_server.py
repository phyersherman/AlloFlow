"""
AlloFlow NPU Inference Server
Runs AI models locally on Snapdragon X NPU via ONNX Runtime + DirectML.
Serves an OpenAI-compatible API on http://localhost:11435

Usage:
  pip install onnxruntime-directml flask huggingface_hub transformers
  python npu_server.py [--model deepseek-r1-1.5b|phi-3.5-mini|qwen-2.5-3b] [--port 11435]

Models auto-download from HuggingFace on first run (~1-3 GB each).
"""

import argparse, json, os, time, uuid
from flask import Flask, request, jsonify

MODELS = {
    "deepseek-r1-1.5b": {
        "repo": "microsoft/DeepSeek-R1-Distill-Qwen-1.5B-onnx",
        "desc": "Best for math reasoning (1.5B, ~40 tok/s on NPU)",
        "ctx": 4096,
    },
    "phi-3.5-mini": {
        "repo": "microsoft/Phi-3.5-mini-instruct-onnx",
        "desc": "Best for general content (3.8B, ~15 tok/s on NPU)",
        "ctx": 4096,
    },
    "qwen-2.5-3b": {
        "repo": "Qwen/Qwen2.5-3B-Instruct-ONNX",
        "desc": "Balanced model (3B params)",
        "ctx": 4096,
    },
}

app = Flask(__name__)
_session = None
_tokenizer = None
_active_id = None


def load_model(model_id):
    global _session, _tokenizer, _active_id
    if model_id == _active_id and _session:
        return
    info = MODELS.get(model_id)
    if not info:
        raise ValueError(f"Unknown model: {model_id}")
    print(f"\n{'='*50}\n  Loading {model_id}\n  {info['desc']}\n{'='*50}")

    import onnxruntime as ort
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer

    cache = os.path.join(os.path.expanduser("~"), ".cache", "alloflow-npu", model_id)
    path = snapshot_download(info["repo"], local_dir=cache)

    # Find ONNX file (prefer int4 quantized)
    onnx_path = None
    for root, _, files in os.walk(path):
        for f in sorted(files):
            if f.endswith(".onnx"):
                if "int4" in f.lower() or not onnx_path:
                    onnx_path = os.path.join(root, f)
    if not onnx_path:
        raise FileNotFoundError(f"No .onnx in {path}")

    opts = ort.SessionOptions()
    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    _session = ort.InferenceSession(
        onnx_path, opts, providers=["DmlExecutionProvider", "CPUExecutionProvider"]
    )
    _tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    _active_id = model_id

    prov = _session.get_providers()[0]
    accel = "NPU/GPU (DirectML)" if "Dml" in prov else "CPU (fallback)"
    print(f"  Accelerator: {accel}\n  Ready!\n")


def generate(messages, max_tokens=1024, temperature=0.7):
    """Simple greedy/sampling generation via ONNX session."""
    import numpy as np
    if not _session or not _tokenizer:
        raise RuntimeError("No model loaded")

    # Build chat prompt
    text = _tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    input_ids = _tokenizer.encode(text, return_tensors="np").astype(np.int64)

    generated = []
    for _ in range(max_tokens):
        inputs = {"input_ids": input_ids}
        # Add attention mask if the model expects it
        for inp in _session.get_inputs():
            if inp.name == "attention_mask":
                inputs["attention_mask"] = np.ones_like(input_ids)
        outputs = _session.run(None, inputs)
        logits = outputs[0][:, -1, :]

        if temperature > 0:
            logits = logits / temperature
            probs = np.exp(logits - np.max(logits))
            probs = probs / probs.sum()
            next_id = np.random.choice(len(probs[0]), p=probs[0])
        else:
            next_id = int(np.argmax(logits[0]))

        if next_id == _tokenizer.eos_token_id:
            break
        generated.append(next_id)
        input_ids = np.concatenate([input_ids, [[next_id]]], axis=1)

    return _tokenizer.decode(generated, skip_special_tokens=True)


# ── OpenAI-compatible endpoints ─────────────────────────────────────

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    data = request.json or {}
    messages = data.get("messages", [])
    max_tokens = data.get("max_tokens", 1024)
    temperature = data.get("temperature", 0.7)

    # Allow switching models via the "model" field
    req_model = data.get("model", "")
    if req_model and req_model in MODELS and req_model != _active_id:
        try:
            load_model(req_model)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    t0 = time.time()
    try:
        reply = generate(messages, max_tokens, temperature)
    except Exception as e:
        return jsonify({"error": {"message": str(e), "type": "server_error"}}), 500

    elapsed = time.time() - t0
    return jsonify({
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": _active_id,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": reply},
            "finish_reason": "stop",
        }],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": len(reply.split()),
            "total_tokens": 0,
        },
        "_alloflow": {"elapsed_s": round(elapsed, 2), "accelerator": _session.get_providers()[0] if _session else "none"},
    })


@app.route("/v1/models", methods=["GET"])
def list_models():
    """List available and active models."""
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": mid,
                "object": "model",
                "owned_by": "alloflow-npu",
                "active": mid == _active_id,
                "description": info["desc"],
            }
            for mid, info in MODELS.items()
        ],
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model": _active_id,
        "accelerator": _session.get_providers()[0] if _session else "none",
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AlloFlow NPU Server")
    parser.add_argument("--model", default="deepseek-r1-1.5b", choices=list(MODELS.keys()),
                        help="Model to load at startup (default: deepseek-r1-1.5b)")
    parser.add_argument("--port", type=int, default=11435, help="Port (default: 11435)")
    args = parser.parse_args()

    print("""
    ╔══════════════════════════════════════════╗
    ║  AlloFlow NPU Inference Server           ║
    ║  ONNX Runtime + DirectML                 ║
    ╚══════════════════════════════════════════╝
    """)
    print(f"  Available models:")
    for mid, info in MODELS.items():
        marker = " ← default" if mid == args.model else ""
        print(f"    • {mid}: {info['desc']}{marker}")
    print()

    try:
        load_model(args.model)
    except ImportError:
        print("\n  ❌ Missing dependencies! Install with:")
        print("     pip install onnxruntime-directml flask huggingface_hub transformers\n")
        exit(1)
    except Exception as e:
        print(f"\n  ❌ Error: {e}")
        print("  Starting without model — use /v1/models to see available models\n")

    print(f"  🌐 Serving on http://localhost:{args.port}")
    print(f"  📡 OpenAI-compatible: /v1/chat/completions")
    print(f"  🔄 Switch models via 'model' field in requests\n")
    app.run(host="0.0.0.0", port=args.port, debug=False)
