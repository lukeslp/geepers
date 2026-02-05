"""
Flask Audio File Upload and Processing Handler

Description: Complete audio file upload, validation, and processing pattern
for speech-to-text, text-to-speech, and audio generation workflows.

Use Cases:
- Speech-to-text transcription (OpenAI Whisper, Assembly AI)
- Text-to-speech generation (OpenAI TTS, ElevenLabs)
- Audio format conversion
- Audio analysis and enhancement

Dependencies:
- flask
- pydub (optional, for audio format conversion)
- mutagen (optional, for audio metadata)

Notes:
- Support common formats: mp3, wav, m4a, ogg, flac
- Consider streaming for large files
- Validate audio duration and sample rate
- Return base64 audio for embedding or URLs for download

Related Snippets:
- flask_multipart_file_upload.py
- base64_audio_encoder.py
- temporary_file_handler.py
- openai_whisper_client.py
"""

from flask import Flask, request, jsonify, send_file
import tempfile
import os
import base64
from typing import Optional, Tuple, Dict
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB for audio
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm'}
MAX_AUDIO_DURATION = 600  # 10 minutes


def allowed_audio_file(filename: str) -> bool:
    """Check if audio file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS


def validate_audio_file(file) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Validate uploaded audio file.

    Returns:
        (is_valid, error_message, metadata)
    """
    if not file or file.filename == '':
        return False, "No audio file selected", None

    if not allowed_audio_file(file.filename):
        return False, f"Audio format not supported. Allowed: {', '.join(ALLOWED_AUDIO_EXTENSIONS)}", None

    # Optional: Validate audio with pydub
    metadata = {}
    try:
        from pydub import AudioSegment
        import io

        audio_bytes = file.read()
        file.seek(0)  # Reset for later reading

        # Detect format from extension
        ext = file.filename.rsplit('.', 1)[1].lower()
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=ext)

        # Get metadata
        metadata = {
            'duration_seconds': len(audio) / 1000.0,
            'channels': audio.channels,
            'sample_rate': audio.frame_rate,
            'sample_width': audio.sample_width,
            'format': ext
        }

        # Validate duration
        if metadata['duration_seconds'] > MAX_AUDIO_DURATION:
            return False, f"Audio too long ({metadata['duration_seconds']:.1f}s). Max: {MAX_AUDIO_DURATION}s", None

    except ImportError:
        # pydub not available, skip validation
        pass
    except Exception as e:
        return False, f"Invalid audio file: {str(e)}", None

    return True, None, metadata


@app.route("/transcribe-audio", methods=["POST"])
def transcribe_audio():
    """
    Transcribe audio to text using speech-to-text.

    Expected form fields:
    - audio: Audio file upload
    - language: Optional language code (default: auto-detect)
    - model: Optional model name (whisper-1, etc.)

    Returns:
        JSON with transcription, language, and metadata
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    is_valid, error, metadata = validate_audio_file(file)

    if not is_valid:
        return jsonify({"error": error}), 400

    language = request.form.get('language', 'auto')
    model = request.form.get('model', 'whisper-1')

    try:
        # Read audio bytes
        audio_bytes = file.read()

        # Save to temporary file (some APIs require file paths)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{metadata.get("format", "mp3")}') as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            # Call speech-to-text service
            result = transcribe_audio_file(tmp_path, language, model)

            return jsonify({
                "success": True,
                "transcription": result['text'],
                "language": result.get('language', language),
                "duration": metadata.get('duration_seconds'),
                "model": model,
                "metadata": metadata
            })

        finally:
            # Clean up temporary file
            try:
                os.remove(tmp_path)
            except:
                pass

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate-speech", methods=["POST"])
def generate_speech():
    """
    Generate speech from text (text-to-speech).

    Expected JSON:
    - text: Text to convert to speech
    - voice: Voice name/ID (default: "alloy")
    - model: TTS model (default: "tts-1")
    - format: Output format (mp3, wav, opus)

    Returns:
        JSON with base64 audio data or download URL
    """
    data = request.get_json()

    text = data.get('text', '').strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400

    voice = data.get('voice', 'alloy')
    model = data.get('model', 'tts-1')
    output_format = data.get('format', 'mp3')

    try:
        # Generate speech
        audio_bytes = generate_tts(text, voice, model, output_format)

        # Option 1: Return base64-encoded audio
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

        return jsonify({
            "success": True,
            "audio_data": audio_base64,
            "format": output_format,
            "size": len(audio_bytes),
            "voice": voice,
            "model": model
        })

        # Option 2: Save and return download URL
        # filename = f"speech_{uuid.uuid4()}.{output_format}"
        # filepath = os.path.join('/tmp', filename)
        # with open(filepath, 'wb') as f:
        #     f.write(audio_bytes)
        # return jsonify({
        #     "success": True,
        #     "audio_url": url_for('download_audio', filename=filename, _external=True),
        #     "format": output_format
        # })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/convert-audio", methods=["POST"])
def convert_audio():
    """
    Convert audio from one format to another.

    Expected form fields:
    - audio: Audio file upload
    - output_format: Target format (mp3, wav, ogg)

    Returns:
        Converted audio file as base64 or download
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    is_valid, error, metadata = validate_audio_file(file)

    if not is_valid:
        return jsonify({"error": error}), 400

    output_format = request.form.get('output_format', 'mp3')
    if output_format not in ALLOWED_AUDIO_EXTENSIONS:
        return jsonify({"error": f"Invalid output format: {output_format}"}), 400

    try:
        from pydub import AudioSegment
        import io

        # Read and convert audio
        audio_bytes = file.read()
        ext = file.filename.rsplit('.', 1)[1].lower()
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=ext)

        # Export to target format
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format=output_format)
        output_bytes = output_buffer.getvalue()

        # Return as base64
        audio_base64 = base64.b64encode(output_bytes).decode('utf-8')

        return jsonify({
            "success": True,
            "audio_data": audio_base64,
            "format": output_format,
            "size": len(output_bytes),
            "original_format": ext
        })

    except ImportError:
        return jsonify({"error": "Audio conversion not available (pydub required)"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/audio-metadata", methods=["POST"])
def audio_metadata():
    """
    Extract metadata from audio file.

    Returns:
        JSON with duration, sample rate, channels, bitrate, etc.
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    is_valid, error, metadata = validate_audio_file(file)

    if not is_valid:
        return jsonify({"error": error}), 400

    return jsonify({
        "success": True,
        "metadata": metadata
    })


# ============================================================================
# PLACEHOLDER FUNCTIONS (Implement with your chosen services)
# ============================================================================

def transcribe_audio_file(audio_path: str, language: str, model: str) -> Dict:
    """
    Transcribe audio using speech-to-text service.

    Example with OpenAI Whisper:
        from openai import OpenAI
        client = OpenAI()
        with open(audio_path, 'rb') as f:
            result = client.audio.transcriptions.create(
                model=model,
                file=f,
                language=language if language != 'auto' else None
            )
        return {"text": result.text, "language": result.language}
    """
    # Placeholder implementation
    return {
        "text": "Transcribed audio content here",
        "language": language
    }


def generate_tts(text: str, voice: str, model: str, output_format: str) -> bytes:
    """
    Generate speech from text.

    Example with OpenAI TTS:
        from openai import OpenAI
        client = OpenAI()
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format=output_format
        )
        return response.content
    """
    # Placeholder implementation
    return b"audio_bytes_here"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
