from flask import Flask, render_template, request, redirect
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')

    if not url:
        return 'URL not provided', 400

    try:
        # Define yt-dlp options to get direct video URL
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'noplaylist': True,
            'quiet': True,
            'get_url': True,  # Get the direct video URL
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)

        if video_url:
            return redirect(video_url)
        else:
            return 'Video URL not found', 500

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
