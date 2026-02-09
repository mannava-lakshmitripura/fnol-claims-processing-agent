from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

from extractor import extract_fields
from router import route_claim

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/process-fnol", methods=["POST"])
def process_fnol():
    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist("files")
    results = []

    for file in files:
        if not file or file.filename == "":
            continue

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        extracted_fields, missing_fields = extract_fields(file_path)
        route, reason = route_claim(extracted_fields, missing_fields)

        results.append({
            "fileName": filename,
            "extractedFields": extracted_fields,
            "missingFields": missing_fields,
            "recommendedRoute": route,
            "reasoning": reason
        })

    return jsonify({
        "totalFiles": len(results),
        "results": results
    })


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    app.run(host=host, port=port, debug=debug)
