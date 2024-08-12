from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    file_name = request.form.get('file_name')
    
    # Debugging output
    print(f"URL: {url}")
    print(f"File Name: {file_name}")
    
    if not url or not file_name:
        return 'URL or file name not provided', 400

    # Define the output file path
    download_dir = 'downloads'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    output_file = os.path.join(download_dir, file_name + '.mp4')
    
    try:
        ydl_opts = {
            'outtmpl': output_file,
            'format': 'best[ext=mp4]',  # Download the best available MP4 format
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return send_file(output_file, as_attachment=True, attachment_filename=file_name + '.mp4')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
