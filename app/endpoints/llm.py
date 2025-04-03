from flask import Blueprint, request, jsonify
import requests

llm_bp = Blueprint('llm', __name__, url_prefix='/api/llm')

@llm_bp.route('/', methods=['POST'])
def query_llm():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input provided'}), 400

    # If the request includes a conversation history as "messages", use it;
    # otherwise, fall back to a single "prompt"
    if 'messages' in data:
        messages = data['messages']
    elif 'prompt' in data:
        messages = [{"role": "user", "content": data["prompt"]}]
    else:
        return jsonify({'error': 'No prompt or messages provided'}), 400

    api_url = ""
    headers = {
        "Content-Type": "application/json",
        "api-key": ""
    }
    payload = {
        "messages": messages,
        "max_completion_tokens": 50000,
        "reasoning_effort": "high"
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "LLM request failed", "details": str(e)}), 500
