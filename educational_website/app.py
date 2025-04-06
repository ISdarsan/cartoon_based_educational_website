from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from pptx import Presentation
from gtts import gTTS
import os
from moviepy.video.io.VideoFileClip import VideoFileClip


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html', dashboard_url=url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload_selection')
def upload_selection():
    return render_template('upload_selection.html')

@app.route('/logout')
def logout():
    # Clear the session or perform logout operations
    session.clear()
    return redirect(url_for('index'))  # Redirect to the index page after logout

@app.route('/')
def index():
    # Your index page logic here
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route("/upload")
def upload_page():
    return render_template("upload_selection.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    ppt_file = request.files['ppt']
    character = request.form['character']
    filename = secure_filename(ppt_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    ppt_file.save(filepath)

    # Extract text from PPT
    prs = Presentation(filepath)
    text = ''
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + ' '

    # Convert text to speech
    tts = gTTS(text)
    audio_path = os.path.join(UPLOAD_FOLDER, 'audio.mp3')
    tts.save(audio_path)

    # Generate a basic video with audio (you can add character image and background later)
    video = ColorClip(size=(1280,720), color=(255,255,255), duration=tts.duration)
    video = video.set_audio(AudioFileClip(audio_path))
    video_path = os.path.join(UPLOAD_FOLDER, 'output.mp4')
    video.write_videofile(video_path, fps=24)

    return send_file(video_path, as_attachment=True)

@app.route("/generate", methods=["POST"])
def generate_audio():
    ppt_file = request.files['ppt']
    ppt_path = os.path.join("uploads", ppt_file.filename)
    ppt_file.save(ppt_path)

    # Extract text
    slides = extract_text_from_ppt(ppt_path)

    audio_files = []
    for i, text in enumerate(slides):
        audio_file = f"static/audio/slide_{i+1}.mp3"
        text_to_audio(text, audio_file)
        audio_files.append(audio_file)

    return jsonify({"status": "success", "audio_files": audio_files})


if __name__ == '__main__':
    app.run(debug=True)
