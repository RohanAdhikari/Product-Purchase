import requests

api_key = "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"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, test."}
    ]
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.text)
