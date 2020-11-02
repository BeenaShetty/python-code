from flask import Flask, render_template, request
import os
app = Flask(__name__)
app.config["IMAGE_UPLOADS"] ="upload"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

@app.route("/")
def hello():
  return render_template('index.html')

# @app.route("/<name>")
# def hello_name(name):
#   return render_template('map.html')

@app.route('/upload', methods=["POST","GET"])
def upload():
  error = None
  success = None
  if request.method == "POST":
    if 'photo' in request.files and request.files['photo'].filename != '':
      upload_photo = request.files['photo']
      if allowed_image(upload_photo.filename):
        upload_photo.save(os.path.join(app.config["IMAGE_UPLOADS"], upload_photo.filename))
        success="File uploaded successfully"
      else:
        error ="This file extension is not allowed"
    else:
      error = "Please select file"
  return render_template("upload.html", error=error, success=success)

@app.route('/multi-upload', methods=["POST","GET"])
def multi_upload():
  success = None
  error = None
  if request.method == "POST" and 'photo' in request.files:
    uploaded_photos = request.files.getlist('photo')
    if len(uploaded_photos) > 2:
      error="Max 2 files are allowed to upload"
    else:
      for photo in uploaded_photos:
        photo.save(os.path.join(app.config["IMAGE_UPLOADS"]+"/multi", photo.filename))
      success = "File uploaded successfully"
  return render_template("multi_upload.html", error=error, success=success)



def allowed_image(filename):
  if not "." in filename:
    return False
  ext = filename.rsplit(".", 1)[1]
  if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
    return True
  else:
    return False

if __name__ == "__main__":
  app.run(debug=True)

