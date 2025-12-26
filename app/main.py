import logging
import os

import dotenv
from flask import Flask, jsonify, render_template, request

# Import New Vision MVP Services
from app.services.vision_service import generate_story_from_image
from app.utils.file_handler import allowed_file, delete_temp_file, save_temp_file

# Initialize Flask app and load environment variables
dotenv.load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


# --- VISION STORY LENS ROUTES ---


@app.route("/", methods=["GET"])
def index():
    """Renders the main landing page for StoryLens."""
    return render_template("index.html")


@app.route("/generate-vision-story", methods=["POST"])
def generate_vision_story():
    """
    Handles photo upload and generates a narrative story using GPT-4o Vision.
    Privacy First: Deletes image immediately after processing.
    """
    file_path = None
    try:
        # 1. Validate Upload
        if "photo" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["photo"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if file and allowed_file(file.filename):
            # 2. Secure Save
            file_path = save_temp_file(file)

            # 3. Extract Metadata
            metadata = {
                "name": request.form.get("name", ""),
                "date": request.form.get("date", ""),
                "note": request.form.get("note", ""),
            }

            # 4. Process with AI (Vision + Story)
            result = generate_story_from_image(file_path, metadata)

            # 5. Return Result
            return jsonify(result)

        else:
            return (
                jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg, webp"}),
                400,
            )

    except Exception as e:
        logging.error(f"Error in vision flow: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        # 6. Privacy Cleanup: ALWAYS delete the file
        if file_path:
            deleted = delete_temp_file(file_path)
            if deleted:
                logging.info(f"Privacy Cleanup: Deleted temp file {file_path}")
            else:
                logging.warning(f"Privacy Cleanup: Failed to delete {file_path}")


# Global exception handler for the Flask app
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error("An error occurred: %s", e)
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
