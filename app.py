from flask import *
import inference
import os
from zipfile import ZipFile

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "outputs"


@app.route("/", methods=["GET"])
def run_app():
    return "Vocal Remover API"


@app.route("/split/", methods=["POST"])
def split_audio():
    if "audio" not in request.files:
        return jsonify({"Status": "Error - No audio file provided"})

    audio_file = request.files["audio"]
    file_name = os.path.join(app.config["UPLOAD_FOLDER"], audio_file.filename)
    audio_file.save(file_name)

    try:
        inference.main(file_name)
    except:
        return jsonify({"Status": "Caught an error in inference.py file!"})

    os.remove(file_name)

    return jsonify({"Status": "Success"})


@app.route("/get/", methods=["GET"])
def get_audio():
    file_name = str(request.args.get("name"))
    instrumental_path = f"outputs/{file_name}_Instruments.wav"
    vocal_path = f"outputs/{file_name}_Vocals.wav"

    zip_filename = f"zip_files/{file_name}_audio_files.zip"

    with ZipFile(zip_filename, "w") as zip_file:
        zip_file.write(instrumental_path)
        zip_file.write(vocal_path)

    response = send_file(zip_filename, as_attachment=True)

    os.remove(instrumental_path)
    os.remove(vocal_path)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
