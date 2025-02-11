from flask import Flask, request, jsonify, render_template
from openai import OpenAI

import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_image_art():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"Error":"No prompt provided by user"}), 400
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    try:
        # Call OpenAI's image generation API using the DALL·E 3 model
        response = client.images.generate(
            prompt=prompt,
            n=1,               # number of images to generate
            size="1024x1024",  # desired output image resolution
            model="dall-e-3"   # specify DALL·E 3 model (ensure your API version supports this)
        )
        # Extract the URL from the API response
        image_url = response.data[0].url
        print(image_url)
        return jsonify({"image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__== "__main__":
    app.run(debug=True)

