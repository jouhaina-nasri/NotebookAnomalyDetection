from flask import Flask, request, send_file
import csv
import os
import sys
import tempfile
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from detector import read_thresholds, analyze_notebook
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        files = request.files.getlist('notebook_files')
        
        if not files:
            return "Aucun fichier sélectionné."
        
        # Créez ou ouvrez le fichier CSV pour écrire les résultats
        csv_file_path = os.path.join(tempfile.gettempdir(), 'results.csv')
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["File", "Cell", "Long Cell", "Long Element Chain", "Complex Container Comprehension", "Long Expression", "Complex IF-Conditional"])

            for file in files:
                file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
                file.save(file_path)
                analyze_notebook(file_path, csv_writer, read_thresholds())

        return send_file(csv_file_path, as_attachment=True)
    

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
