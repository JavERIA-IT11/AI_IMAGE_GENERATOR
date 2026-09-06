from dotenv import load_dotenv
import os
import requests
import base64

from flask import Flask, request, jsonify, render_template


# Load .env file
load_dotenv()

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_image():

    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({
            "error": "Please enter a prompt."
        }), 400

    try:

        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
        )

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt
            },
            timeout=120
        )

        if response.status_code != 200:
            return jsonify({
                "error": response.text
            }), 500

        result = response.json()

        image_base64 = result.get("result", {}).get("image")

        if not image_base64:
            return jsonify({
                "error": "No image was returned."
            }), 500

        return jsonify({
            "image": image_base64
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
