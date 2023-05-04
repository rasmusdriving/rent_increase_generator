from flask import Flask, render_template, request, send_from_directory, url_for
import os
import json
from datetime import datetime
from rent_utils import extract_info_from_pdf, create_new_rent_increase_pdf

app = Flask(__name__)

@app.route('/')
def index():
    preload_js = url_for('static', filename='preload.js')
    return render_template('index.html', preload_js=preload_js)


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        upload_dir = os.path.join('app', 'uploaded_files')
        os.makedirs(upload_dir, exist_ok=True)
        uploaded_file.save(os.path.join(upload_dir, uploaded_file.filename))
    response = {
        'filename': uploaded_file.filename
    }
    return json.dumps(response)


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    filename = data['filename']
    new_rent = data['new_rent']
    application_date = datetime.strptime(data['application_date'], '%Y-%m-%d')

    pdf_path = os.path.join('app', 'uploaded_files', filename)
    landlord_name, tenant_name, address, transaction_id, current_rent = extract_info_from_pdf(pdf_path)
    downloads_folder = os.path.expanduser('~/Downloads')
    output_file_name = f"Rent_Increase_{transaction_id}.docx"
    output_path = os.path.join(downloads_folder, output_file_name)

    service_fee = new_rent * 0.0495
    template_path = os.path.join('app', 'template.docx')
    
    create_new_rent_increase_pdf(template_path, landlord_name, tenant_name, application_date, current_rent, new_rent, service_fee, address, transaction_id, output_path)    
    response = {
        'status': 'success',
        'output_path': output_file_name
    }
    return json.dumps(response)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(directory='downloads', filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

