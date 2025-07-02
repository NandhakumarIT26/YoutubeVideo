from flask import Flask, render_template, request, send_file
import os
import uuid
import yt_dlp

app = Flask(__name__)

# Folder where downloaded videos will be stored
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(video_url, file_name):
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'merge_output_format': 'mp4',
        'outtmpl': file_name,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]
        if not video_url:
            return render_template("index.html", message="Please enter a valid URL.")

        # Generate a unique filename
        file_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.mp4")

        try:
            download_video(video_url, output_path)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return render_template("index.html", message=f"Error: {str(e)}")

    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)