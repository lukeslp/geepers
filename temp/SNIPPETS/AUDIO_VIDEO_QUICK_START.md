# Audio/Video Feature Quick Start Guide

**For**: Implementing audio and video features in Studio and other services
**Date**: 2025-11-15
**Status**: Ready for implementation

## Overview

This guide shows how to use the newly harvested snippets to add audio/video capabilities to your Flask applications.

## Available Patterns

### 1. Audio Features

**Snippets**:
- `/home/coolhand/SNIPPETS/web-frameworks/flask_audio_file_handler.py`
- `/home/coolhand/SNIPPETS/web-frameworks/flask_multipart_file_upload.py`
- `/home/coolhand/SNIPPETS/web-frameworks/javascript_loading_states_pattern.js`

**Capabilities**:
- Speech-to-text (Whisper, Assembly AI, etc.)
- Text-to-speech (OpenAI TTS, ElevenLabs)
- Audio format conversion
- Audio metadata extraction

**Quick Implementation** (5 minutes):

```python
# Copy the audio handler pattern
cp ~/SNIPPETS/web-frameworks/flask_audio_file_handler.py studio/audio_routes.py

# Install dependencies
pip install pydub mutagen

# Add to your Flask app
from audio_routes import transcribe_audio, generate_speech

app.register_blueprint(audio_bp, url_prefix='/audio')
```

### 2. Video Features

**Snippets**:
- `/home/coolhand/SNIPPETS/web-frameworks/flask_video_generation_handler.py`
- `/home/coolhand/SNIPPETS/utilities/cache_manager_redis_fallback.py`

**Capabilities**:
- AI video generation (xAI, future OpenAI Sora)
- Video upload and analysis
- Thumbnail extraction
- Video format conversion

**Quick Implementation** (5 minutes):

```python
# Copy the video handler pattern
cp ~/SNIPPETS/web-frameworks/flask_video_generation_handler.py studio/video_routes.py

# Install dependencies
pip install opencv-python

# Add to your Flask app
from video_routes import generate_video, analyze_video

app.register_blueprint(video_bp, url_prefix='/video')
```

### 3. Frontend Loading States

**Snippet**: `/home/coolhand/SNIPPETS/web-frameworks/javascript_loading_states_pattern.js`

**Quick Implementation** (2 minutes):

```html
<!-- Copy loading state patterns -->
<script src="{{ url_for('static', filename='loading_states.js') }}"></script>

<script>
// Use with audio upload
async function uploadAudio() {
    const btn = new ButtonState('upload-btn');
    btn.loading('Uploading...');

    try {
        const result = await uploadFileWithProgress(file, '/audio/transcribe');
        btn.success('Transcribed!');
        displayResult(result);
    } catch (error) {
        btn.error('Failed');
        showToast(error.message, 'error');
    }
}
</script>
```

## Complete Example: Add TTS to Studio

### Step 1: Backend Route (5 minutes)

```python
# studio/app.py

@studio_bp.route("/generate-speech", methods=["POST"])
def generate_speech():
    """Generate speech from text using OpenAI TTS"""
    data = request.get_json()

    text = data.get('text', '').strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400

    voice = data.get('voice', 'alloy')
    model = data.get('model', 'tts-1')

    # Check cache first
    cache_key_data = [text, voice, model]
    cached = cache.get('tts', 'openai', cache_key_data)
    if cached:
        return jsonify(cached)

    try:
        # Generate speech with OpenAI
        from openai import OpenAI
        client = OpenAI()

        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        # Convert to base64
        import base64
        audio_base64 = base64.b64encode(response.content).decode('utf-8')

        result = {
            "audio_data": audio_base64,
            "voice": voice,
            "model": model,
            "format": "mp3"
        }

        # Cache for 2 hours
        cache.set('tts', 'openai', cache_key_data, result, ttl=7200)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Step 2: Frontend UI (5 minutes)

```html
<!-- Add to templates/index.html -->

<!-- TTS Mode -->
<div class="mode-content" id="tts-mode">
    <div class="controls card">
        <div class="control-group">
            <label for="tts-text">Text to Speak</label>
            <textarea id="tts-text" placeholder="Enter text to convert to speech..."></textarea>
        </div>

        <div class="control-group">
            <label for="tts-voice">Voice</label>
            <select id="tts-voice">
                <option value="alloy">Alloy (Neutral)</option>
                <option value="echo">Echo (Male)</option>
                <option value="fable">Fable (British Male)</option>
                <option value="onyx">Onyx (Deep Male)</option>
                <option value="nova">Nova (Female)</option>
                <option value="shimmer">Shimmer (Soft Female)</option>
            </select>
        </div>

        <button class="btn btn-primary" onclick="generateSpeech()">Generate Speech</button>
    </div>

    <div class="loading" id="tts-loading">
        <div class="spinner"></div>
        <span>Generating speech...</span>
    </div>

    <div class="status" id="tts-status"></div>

    <!-- Audio player -->
    <div class="output-area" id="tts-output">
        <audio id="tts-audio" controls style="width: 100%; display: none;"></audio>
    </div>
</div>

<script>
async function generateSpeech() {
    const text = document.getElementById('tts-text').value.trim();
    if (!text) {
        showStatus('tts-status', 'error', 'Please enter text');
        return;
    }

    const voice = document.getElementById('tts-voice').value;
    const loadingEl = document.getElementById('tts-loading');
    const statusEl = document.getElementById('tts-status');
    const audioEl = document.getElementById('tts-audio');

    loadingEl.classList.add('visible');
    statusEl.classList.remove('visible');
    audioEl.style.display = 'none';

    try {
        const response = await fetch('/io/studio/generate-speech', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, voice, model: 'tts-1' })
        });

        const data = await response.json();

        if (response.ok) {
            // Set audio source
            audioEl.src = 'data:audio/mpeg;base64,' + data.audio_data;
            audioEl.style.display = 'block';
            audioEl.play();

            showStatus('tts-status', 'success', '✅ Speech generated!');
        } else {
            showStatus('tts-status', 'error', '❌ ' + data.error);
        }

    } catch (error) {
        showStatus('tts-status', 'error', '❌ ' + error.message);
    } finally {
        loadingEl.classList.remove('visible');
    }
}
</script>
```

### Step 3: Test (1 minute)

```bash
# Restart Studio
cd /home/coolhand/servers/studio
./studio.sh restart

# Open browser
# https://dr.eamer.dev/io/studio
# Navigate to TTS tab
# Enter text, select voice, click "Generate Speech"
```

**Total Time**: ~11 minutes from snippet to working feature

## Integration with Existing Studio Components

### Using Provider Adapter Pattern

```python
# providers/studio_adapters.py

class OpenAIAdapter(StudioProviderAdapter):
    def generate_speech(self, text: str, voice: str = 'alloy', **kwargs):
        """Add TTS to OpenAI adapter"""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)

        response = client.audio.speech.create(
            model=kwargs.get('model', 'tts-1'),
            voice=voice,
            input=text
        )

        return response.content

    def transcribe_audio(self, audio_file, **kwargs):
        """Add speech-to-text to OpenAI adapter"""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)

        with open(audio_file, 'rb') as f:
            result = client.audio.transcriptions.create(
                model=kwargs.get('model', 'whisper-1'),
                file=f
            )

        return result.text
```

### Using Cache Manager

```python
# Already integrated in Studio!
from cache_manager import CacheManager

cache = CacheManager(use_redis=True, key_prefix="studio")

# Automatic caching in TTS endpoint
cached = cache.get('tts', 'openai', cache_key_data)
if cached:
    return jsonify(cached)  # 40-100x cost savings

# ... generate speech ...

cache.set('tts', 'openai', cache_key_data, result, ttl=7200)
```

## Provider Comparison

| Provider | TTS | Speech-to-Text | Voices | Quality | Cost |
|----------|-----|----------------|--------|---------|------|
| OpenAI | ✅ tts-1, tts-1-hd | ✅ whisper-1 | 6 | Excellent | $15/1M chars |
| ElevenLabs | ✅ | ❌ | 100+ | Outstanding | $22/1M chars |
| xAI | Planned | Planned | TBD | TBD | TBD |
| Google | ✅ | ✅ | 400+ | Very Good | $4/1M chars |

## Next Steps

1. **Immediate** (Today):
   - Add TTS to Studio using OpenAI
   - Add speech-to-text endpoint
   - Test with frontend

2. **Short-term** (This Week):
   - Add video generation when xAI releases API
   - Implement video thumbnail extraction
   - Add audio format conversion

3. **Medium-term** (This Month):
   - Add ElevenLabs provider for premium voices
   - Implement video analysis with Gemini
   - Create audio/video library in Studio

4. **Long-term** (Next Quarter):
   - Extend shared library with audio/video mixins
   - Create media_utils module
   - Add cache decorator to shared library

## Troubleshooting

### Audio Not Playing in Browser

```javascript
// Check audio format compatibility
if (!audioEl.canPlayType('audio/mpeg')) {
    // Convert to supported format
    // Or use different format in TTS generation
}
```

### Large Audio Files Timing Out

```python
# Use streaming response
from flask import Response

@app.route('/generate-speech-stream')
def generate_speech_stream():
    def generate():
        # Stream audio chunks
        for chunk in audio_generator():
            yield chunk

    return Response(generate(), mimetype='audio/mpeg')
```

### Redis Not Available

```python
# Cache manager automatically falls back to in-memory
cache = CacheManager(use_redis=True)  # Will use memory if Redis unavailable

# Check cache backend
stats = cache.get_stats()
print(f"Using {stats['backend']} cache")  # "redis" or "memory"
```

## Resources

- **Snippets**: `/home/coolhand/SNIPPETS/`
- **Studio Source**: `/home/coolhand/servers/studio/`
- **Extraction Report**: `/home/coolhand/SNIPPETS/EXTRACTION_STUDIO_2025-11-15.md`
- **OpenAI TTS Docs**: https://platform.openai.com/docs/guides/text-to-speech
- **Whisper API Docs**: https://platform.openai.com/docs/guides/speech-to-text

## Questions?

- Check the snippet header comments for detailed usage
- Review the extraction report for design patterns
- Test snippets in isolation before integration
- Use cache manager to reduce API costs
