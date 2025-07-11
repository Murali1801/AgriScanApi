# AgriAPI

A Flask API for crop leaf image diagnostics using OpenRouter's Qwen2.5 VL 32B Instruct model.

## Features
- Accepts crop leaf images via API
- Sends images and expert prompt to OpenRouter for analysis
- Returns structured JSON with crop health, disease, and remedy info
- CORS enabled for https://agri-scan-api.vercel.app and localhost

## Setup

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a `.env` file** in the project root:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

## Running the Server

```bash
python app.py
```

The server will run at `http://127.0.0.1:5000` by default.

## API Usage

### Endpoint
`POST /analyze-leaf`

### Request
- **Content-Type:** `multipart/form-data`
- **Field:** `image` (the crop leaf image file)

### Example with `curl`
```bash
curl -X POST http://127.0.0.1:5000/analyze-leaf \
  -F "image=@your_leaf_image.jpg"
```

### Response
- JSON object with crop health, disease info, and recommendations, or error message.

## CORS
Allowed origins:
- https://agri-scan-api.vercel.app
- http://localhost
- http://localhost:3000

## License
MIT 