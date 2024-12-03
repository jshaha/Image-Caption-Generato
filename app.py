from flask import Flask, request, render_template, session
import openai
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Set up OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

# Function to encode the image in base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Ensure upload directory exists
        os.makedirs("static/uploads", exist_ok=True)

         # Check if a new image was uploaded
        if 'image' in request.files and request.files['image'].filename != '':
            # Get the uploaded image and save it
            image = request.files['image']
            image_path = os.path.join("static/uploads", image.filename)
            image.save(image_path)  # Save the image locally
            session['last_image'] = image_path  # Store the image path in session
        else:
            # Use the last uploaded image if no new image is uploaded
            image_path = session.get('last_image')
            if not image_path:
                return "No image uploaded yet. Please upload an image first."

        # Step 1: Encode the image in base64
        base64_image = encode_image(image_path)

        # Step 2: Send the base64 image to OpenAI for caption generation
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Correct model with base64 image input support
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Generate an Instagram-style caption for this image."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ]
                }
            ]
        )
        print(response.choices[0])
        # Extract the generated caption
        caption = response.choices[0].message.content if response.choices else "Caption generation failed."


        # Display the image and generated caption in the HTML template
        return render_template("index.html", image=image_path, caption=caption)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
