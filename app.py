from flask import Flask, request, render_template
import boto3
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET_NAME = "spongebob-25"
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt'}

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        error_message = "No file selected."
        print(error_message)  # Log the error
        return render_template('index.html', error=error_message)

    file = request.files['file']
    if file:
        print(f"Received file: {file.filename}")  # Log the file name
        
        if allowed_files(file.filename):
            filename = secure_filename(file.filename)
            try:
                print(f"Attempting to upload {filename} to S3...")
                s3.upload_fileobj(file, BUCKET_NAME, filename)
                
                file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
                print(f"File uploaded successfully! Accessible at {file_url}")
                
                return render_template("index.html", file_url=file_url)
            except Exception as e:
                print(f"Error during upload: {str(e)}")
                return render_template("index.html", error=f"Error uploading file: {str(e)}")
        else:
            error_message = "File type not allowed."
            print(error_message)  # Log the error
            return render_template("index.html", error=error_message)
    else:
        error_message = "No file selected."
        print(error_message)  # Log the error
        return render_template("index.html", error=error_message)


if __name__ == '__main__':
    app.run(debug=True)
