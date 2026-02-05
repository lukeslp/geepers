"""
Flask Multipart File Upload Handler

Description: Robust file upload handling with validation, type checking,
and error handling. Supports multiple file types and size limits.

Use Cases:
- Image upload for AI vision models
- Audio file upload for speech-to-text
- Video upload for processing
- Document upload for analysis

Dependencies:
- flask
- PIL (optional, for image validation)

Notes:
- Always validate file.filename != '' before processing
- Use file.read() once, don't call multiple times
- Consider file size limits (request.max_content_length)
- Sanitize filenames for security

Related Snippets:
- base64_image_encoder.py
- file_type_validator.py
- temporary_file_handler.py
"""

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
from typing import Optional, Tuple

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp3', 'wav', 'mp4'}


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_uploaded_file(file) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded file.

    Returns:
        (is_valid, error_message)
    """
    # Check if file exists
    if not file:
        return False, "No file provided"

    # Check if filename is empty (happens when no file selected)
    if file.filename == '':
        return False, "No file selected"

    # Check file extension
    if not allowed_file(file.filename):
        return False, f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"

    return True, None


@app.route("/upload-image", methods=["POST"])
def upload_image():
    """
    Handle image upload with validation.

    Expected form fields:
    - image: File upload
    - prompt: Optional text field
    """
    # Check if file is in request
    if 'image' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['image']

    # Validate file
    is_valid, error = validate_uploaded_file(file)
    if not is_valid:
        return jsonify({"error": error}), 400

    # Get optional form fields
    prompt = request.form.get('prompt', 'Describe this image')

    try:
        # Read file data (do this ONCE)
        file_bytes = file.read()

        # Optional: Validate image with PIL
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()  # Verify it's a valid image
            width, height = img.size
        except Exception as e:
            return jsonify({"error": f"Invalid image file: {str(e)}"}), 400

        # Process the file
        # Example: Convert to base64
        import base64
        file_base64 = base64.b64encode(file_bytes).decode('utf-8')

        # Or save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            # Process file at tmp_path
            result = process_image(tmp_path, prompt)

            return jsonify({
                "success": True,
                "result": result,
                "filename": secure_filename(file.filename),
                "size": len(file_bytes),
                "dimensions": f"{width}x{height}"
            })
        finally:
            # Clean up temporary file
            try:
                os.remove(tmp_path)
            except:
                pass

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """
    Handle audio upload for speech-to-text or audio generation.

    Expected form fields:
    - audio: File upload
    - language: Optional language code
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    is_valid, error = validate_uploaded_file(file)
    if not is_valid:
        return jsonify({"error": error}), 400

    language = request.form.get('language', 'en')

    try:
        audio_bytes = file.read()

        # Process audio
        result = process_audio(audio_bytes, language)

        return jsonify({
            "success": True,
            "result": result,
            "filename": secure_filename(file.filename),
            "size": len(audio_bytes)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload-multiple", methods=["POST"])
def upload_multiple():
    """Handle multiple file uploads"""
    # Check if files exist
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('files')

    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected"}), 400

    results = []
    errors = []

    for file in files:
        is_valid, error = validate_uploaded_file(file)
        if not is_valid:
            errors.append({"filename": file.filename, "error": error})
            continue

        try:
            file_bytes = file.read()
            # Process each file
            result = {
                "filename": secure_filename(file.filename),
                "size": len(file_bytes),
                "status": "processed"
            }
            results.append(result)
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})

    return jsonify({
        "success": len(results) > 0,
        "processed": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    })


# Placeholder processing functions
def process_image(image_path: str, prompt: str) -> dict:
    """Process image with AI vision model"""
    # Implement your image processing logic
    return {"description": "Image processed"}


def process_audio(audio_bytes: bytes, language: str) -> dict:
    """Process audio with speech-to-text"""
    # Implement your audio processing logic
    return {"transcription": "Audio processed"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
