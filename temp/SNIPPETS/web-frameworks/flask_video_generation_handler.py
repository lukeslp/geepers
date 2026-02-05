"""
Flask Video Generation and Upload Handler

Description: Video upload, processing, and generation handler for AI video
models and video analysis workflows.

Use Cases:
- AI video generation (image-to-video, text-to-video)
- Video upload for analysis
- Video format conversion
- Thumbnail generation

Dependencies:
- flask
- opencv-python (optional, for video processing)
- ffmpeg-python (optional, for video conversion)

Notes:
- Large file sizes require careful handling
- Consider streaming uploads for large videos
- Video generation is often async - use task queue or polling
- Return video URLs instead of base64 for large files

Related Snippets:
- flask_multipart_file_upload.py
- async_task_queue.py
- video_thumbnail_generator.py
"""

from flask import Flask, request, jsonify, url_for
import tempfile
import os
import uuid
from typing import Optional, Tuple, Dict
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB for video
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'webm', 'mkv'}
VIDEO_STORAGE_PATH = '/tmp/videos'
MAX_VIDEO_DURATION = 300  # 5 minutes

# Ensure storage directory exists
os.makedirs(VIDEO_STORAGE_PATH, exist_ok=True)


def allowed_video_file(filename: str) -> bool:
    """Check if video file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS


def validate_video_file(file) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Validate uploaded video file.

    Returns:
        (is_valid, error_message, metadata)
    """
    if not file or file.filename == '':
        return False, "No video file selected", None

    if not allowed_video_file(file.filename):
        return False, f"Video format not supported. Allowed: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}", None

    metadata = {}

    # Optional: Validate with OpenCV
    try:
        import cv2
        import numpy as np

        # Save to temp file for validation
        video_bytes = file.read()
        file.seek(0)  # Reset for later reading

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        try:
            cap = cv2.VideoCapture(tmp_path)

            if not cap.isOpened():
                return False, "Invalid video file", None

            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0

            metadata = {
                'duration_seconds': duration,
                'fps': fps,
                'frame_count': frame_count,
                'width': width,
                'height': height,
                'resolution': f'{width}x{height}',
                'size_bytes': len(video_bytes)
            }

            cap.release()

            # Validate duration
            if duration > MAX_VIDEO_DURATION:
                return False, f"Video too long ({duration:.1f}s). Max: {MAX_VIDEO_DURATION}s", None

        finally:
            os.remove(tmp_path)

    except ImportError:
        # OpenCV not available
        pass
    except Exception as e:
        return False, f"Error validating video: {str(e)}", None

    return True, None, metadata


@app.route("/generate-video", methods=["POST"])
def generate_video():
    """
    Generate video from text or image using AI.

    Expected JSON:
    - prompt: Text description of video
    - image_data: Optional base64 image for image-to-video
    - duration: Video duration in seconds
    - model: AI model to use (default: "xai-video")

    Returns:
        JSON with video URL or task ID for async generation
    """
    data = request.get_json()

    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    image_data = data.get('image_data')
    duration = data.get('duration', 5)
    model = data.get('model', 'xai-video')

    try:
        # Option 1: Synchronous generation (if fast enough)
        result = generate_video_ai(prompt, image_data, duration, model)

        if result.get('success'):
            # Save video to storage
            video_id = str(uuid.uuid4())
            video_path = os.path.join(VIDEO_STORAGE_PATH, f'{video_id}.mp4')

            with open(video_path, 'wb') as f:
                f.write(result['video_bytes'])

            return jsonify({
                "success": True,
                "video_url": url_for('download_video', video_id=video_id, _external=True),
                "video_id": video_id,
                "duration": duration,
                "model": model
            })
        else:
            return jsonify({"error": result.get('error', 'Unknown error')}), 500

        # Option 2: Asynchronous generation with task queue
        # from celery_app import generate_video_task
        # task = generate_video_task.delay(prompt, image_data, duration, model)
        # return jsonify({
        #     "success": True,
        #     "task_id": task.id,
        #     "status_url": url_for('video_status', task_id=task.id, _external=True)
        # }), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze-video", methods=["POST"])
def analyze_video():
    """
    Analyze video content with AI.

    Expected form fields:
    - video: Video file upload
    - prompt: Analysis prompt (optional)

    Returns:
        JSON with analysis results
    """
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    is_valid, error, metadata = validate_video_file(file)

    if not is_valid:
        return jsonify({"error": error}), 400

    prompt = request.form.get('prompt', 'Describe this video in detail')

    try:
        video_bytes = file.read()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        try:
            # Analyze video
            result = analyze_video_ai(tmp_path, prompt, metadata)

            return jsonify({
                "success": True,
                "analysis": result['description'],
                "metadata": metadata,
                "key_frames": result.get('key_frames', [])
            })

        finally:
            os.remove(tmp_path)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/video-thumbnail", methods=["POST"])
def video_thumbnail():
    """
    Generate thumbnail from video.

    Expected form fields:
    - video: Video file upload
    - timestamp: Optional timestamp for frame extraction (default: 0)

    Returns:
        JSON with base64 thumbnail image
    """
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    is_valid, error, metadata = validate_video_file(file)

    if not is_valid:
        return jsonify({"error": error}), 400

    timestamp = float(request.form.get('timestamp', 0))

    try:
        import cv2
        import base64

        video_bytes = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        try:
            cap = cv2.VideoCapture(tmp_path)
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Seek to timestamp
            frame_number = int(timestamp * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

            ret, frame = cap.read()
            cap.release()

            if not ret:
                return jsonify({"error": "Could not extract frame"}), 500

            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            thumbnail_base64 = base64.b64encode(buffer).decode('utf-8')

            return jsonify({
                "success": True,
                "thumbnail": thumbnail_base64,
                "timestamp": timestamp,
                "width": frame.shape[1],
                "height": frame.shape[0]
            })

        finally:
            os.remove(tmp_path)

    except ImportError:
        return jsonify({"error": "Thumbnail generation not available (cv2 required)"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download-video/<video_id>")
def download_video(video_id):
    """Download generated video"""
    # Validate video_id to prevent directory traversal
    if not video_id.replace('-', '').replace('_', '').isalnum():
        return jsonify({"error": "Invalid video ID"}), 400

    video_path = os.path.join(VIDEO_STORAGE_PATH, f'{video_id}.mp4')

    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404

    return send_file(
        video_path,
        mimetype='video/mp4',
        as_attachment=True,
        download_name=f'{video_id}.mp4'
    )


# ============================================================================
# PLACEHOLDER FUNCTIONS
# ============================================================================

def generate_video_ai(
    prompt: str,
    image_data: Optional[str],
    duration: int,
    model: str
) -> Dict:
    """
    Generate video using AI service.

    Example with xAI (when available):
        from openai import OpenAI
        client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
        response = client.videos.generate(
            model=model,
            prompt=prompt,
            duration=duration
        )
        return {"success": True, "video_bytes": response.content}
    """
    # Placeholder
    return {
        "success": False,
        "error": "Video generation not yet implemented"
    }


def analyze_video_ai(video_path: str, prompt: str, metadata: Dict) -> Dict:
    """
    Analyze video with AI vision model.

    Example: Extract key frames and analyze each with vision model
    """
    return {
        "description": "Video analysis placeholder",
        "key_frames": []
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
