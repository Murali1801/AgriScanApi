import os
import base64
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
CORS(app, origins=[
    "https://agri-scan-api.vercel.app",
    "http://localhost",
    "http://localhost:3000",
    "https://agri-scan-ai.vercel.app"
])

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

PROMPT = """
You are a highly accurate agricultural diagnostics assistant trained in advanced crop science and plant pathology.

Your task is to analyze a crop leaf image and provide expert-level diagnostics. Follow the steps below carefully:

---

1. Identify the crop type based on visual features of the leaf. Use domain knowledge of crop leaf patterns, shapes, and texture. Be confident and only choose from known crops (e.g., rice, tomato, potato, corn, wheat, chili, brinjal, etc.).

2. Assess plant health:
   - If healthy, mention clearly.
   - If diseased, determine:
     - Disease name (e.g., blight, rust, mildew)
     - Symptoms observed (e.g., brown spots, curling, yellowing, powdery layer)
     - Severity (%) — approximate the percentage of the leaf area affected

3. Give treatment recommendations:
   - Chemical remedy: Name of pesticide or fungicide with correct dosage
   - Organic remedy: A natural treatment (e.g., neem oil, compost tea)
   - Preventive measures: Crop rotation, proper spacing, sunlight, watering tips
   - Recommended action: e.g., Monitor, Isolate plant, Apply spray, Remove infected parts

---

📦 Return your complete diagnosis strictly in one of the following JSON formats:

✅ If the crop is healthy:
{
  "crop": "<crop name>",
  "status": "healthy",
  "message": "The crop appears healthy with no visible symptoms.",
  "recommended_practices": "Maintain regular inspection, use compost, and follow crop rotation to ensure ongoing health."
}

⚠️ If the crop is diseased:
{
  "crop": "<crop name>",
  "status": "diseased",
  "disease_name": "<name of disease>",
  "symptoms": "<list of visual symptoms>",
  "affected_percentage": "<approximate percentage>",
  "chemical_remedy": "<fungicide or pesticide and dosage>",
  "organic_remedy": "<natural/organic remedy>",
  "preventive_measures": "<steps to avoid recurrence>",
  "recommended_action": "<next step the farmer should take>"
}

❌ If the image is invalid or not a crop leaf:
{
  "error": "Invalid image or not related to crop leaves. Please upload a clear image."
}

---

Only respond using one of the above JSON structures. Do not include any explanation, formatting, or additional comments.
"""

@app.route('/analyze-leaf', methods=['POST'])
def analyze_leaf():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image_bytes = image.read()
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')

    # Prepare the payload for OpenRouter
    payload = {
        "model": "qwen/qwen2.5-vl-32b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:{image.mimetype};base64,{image_b64}"
                    }
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}" if OPENROUTER_API_KEY else "",
        "Content-Type": "application/json"
    }

    openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

    response = requests.post(openrouter_url, headers=headers, json=payload)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to get response from OpenRouter', 'details': response.text}), 500

    # Extract only the 'content' field from the response
    try:
        data = response.json()
        content = data['choices'][0]['message']['content']
        # Try to parse the content as JSON
        import json as _json
        try:
            content_json = _json.loads(content)
            return jsonify(content_json)
        except Exception:
            return content  # If not valid JSON, return as string
    except Exception as e:
        return jsonify({'error': 'Unexpected response format', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 