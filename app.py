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
    print(f"Current Working Directory: {os.getcwd()}")
    
    if not url or not file_name:
        return 'URL or file name not provided', 400

    # Define the output file path
    download_dir = os.path.join(os.getcwd(), 'downloads')
    print(f"Download Directory: {download_dir}")

    if not os.path.exists(download_dir):
        print(f"Directory does not exist. Creating: {download_dir}")
        os.makedirs(download_dir)
    
    output_file = os.path.join(download_dir, file_name + '.mp4')
    print(f"Output File Path: {output_file}")
    
    try:
        ydl_opts = {
            'outtmpl': output_file,
            'format': 'best[ext=mp4]',  # Download the best available MP4 format
            'noplaylist': True,
            'quiet': True,  # Set to False for detailed output
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Verify file existence
        if not os.path.isfile(output_file):
            return 'File not found on server', 404
        
        # Send file as an attachment for download
        return send_file(
            output_file,
            as_attachment=True,
            download_name=file_name + '.mp4',  # Use download_name instead of attachment_filename
            mimetype='video/mp4'
        )
    except Exception as e:
        print(f"Error: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
