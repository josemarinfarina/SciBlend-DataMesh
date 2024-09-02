import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import DataMesh

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'csv', 'obj'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'csv_file' not in request.files or 'obj_file' not in request.files:
            return jsonify({'success': False, 'message': 'Not all required files were selected'})
        
        csv_file = request.files['csv_file']
        obj_file = request.files['obj_file']
        
        start_frame = int(request.form.get('start_frame', 0))
        end_frame = int(request.form.get('end_frame', -1))
        
        if csv_file.filename == '' or obj_file.filename == '':
            return jsonify({'success': False, 'message': 'Not all required files were selected'})
        
        if csv_file and allowed_file(csv_file.filename) and obj_file and allowed_file(obj_file.filename):
            csv_filename = secure_filename(csv_file.filename)
            obj_filename = secure_filename(obj_file.filename)
            
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
            obj_path = os.path.join(app.config['UPLOAD_FOLDER'], obj_filename)
            
            csv_file.save(csv_path)
            obj_file.save(obj_path)
            
            case_id = os.path.splitext(obj_filename)[0]
            output_folder = os.path.join(app.config['OUTPUT_FOLDER'], case_id)
            
            try:
                if not os.path.exists(csv_path) or not os.path.exists(obj_path):
                    return jsonify({'success': False, 'message': f'Error: Could not save files. CSV: {os.path.exists(csv_path)}, OBJ: {os.path.exists(obj_path)}'})
                
                processing_result = DataMesh.process_files(app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'], case_id, csv_filename, obj_filename, start_frame, end_frame)
                
                if processing_result:
                    if os.path.exists(output_folder):
                        files_in_output = os.listdir(output_folder)
                        if files_in_output:
                            return jsonify({'success': True, 'message': f'Files processed. Results are in the folder {output_folder}. Generated files: {", ".join(files_in_output)}'})
                        else:
                            return jsonify({'success': False, 'message': f'Processing completed, but no VTK files were generated in the output folder {output_folder}. Please check the server logs.'})
                    else:
                        return jsonify({'success': False, 'message': f'Processing completed, but the output folder {output_folder} was not created. Please check the server logs.'})
                else:
                    return jsonify({'success': False, 'message': f'Processing failed. Please check the server logs for more details. Contents of the upload folder: {", ".join(os.listdir(app.config["UPLOAD_FOLDER"]))}'})
            except Exception as e:
                return jsonify({'success': False, 'message': f'An error occurred during processing: {str(e)}'})
    
    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)