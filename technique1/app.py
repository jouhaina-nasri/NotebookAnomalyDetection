from flask import Flask, request, send_file
import csv
import os
import sys
sys.path.append('.')
from detector import read_thresholds, analyze_notebook
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = '/app/uploads'
@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        files = request.files.getlist('notebook_files')
        
        if not files:
            return "Aucun fichier sélectionné."
        
        # Créez ou ouvrez le fichier CSV pour écrire les résultats
        csv_file_path = '/app/results.csv'
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["File", "Cell", "Long Cell", "Complex Container Comprehension", "Long Element Chain", "Long Expression", "Complex IF-Conditional"])

            for file in files:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                analyze_notebook(file_path, csv_writer, read_thresholds())

        return send_file(csv_file_path, as_attachment=True)
    

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
