import requests

url = "http://127.0.0.1:5000/analyze-leaf"
image_path = "your_leaf_image.jpg"  # Replace with your image path

with open(image_path, "rb") as img:
    files = {"image": img}
    response = requests.post(url, files=files)

print("Status code:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("Raw response:", response.text) 