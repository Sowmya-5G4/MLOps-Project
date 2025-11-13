from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image
import os
import google.generativeai as genai

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['GENERATIVE_API_KEY'] = 'AIzaSyCc4nwwo9RnY3J3YrWdo3DGh91fU_dPz_o'
app.config['GEN_MODEL_NAME'] = 'gemini-1.5-flash'

genai.configure(api_key=app.config['GENERATIVE_API_KEY'])
genModel = genai.GenerativeModel(app.config['GEN_MODEL_NAME'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            response = geminiResponse(file_path, request.form['prompt'])
           # excel_filename = f"table_data_{filename}.xlsx"
           # write_to_excel(response, excel_filename)
            return render_template('index.html', poem=response, image_filename=filename)
    return render_template('index.html', poem=None, image_filename=None)

def geminiResponse(image_path, prompt):
    image = Image.open(image_path)
    response = genModel.generate_content([prompt, image])
    return response.text

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# def write_to_excel(table_data_string, excel_filename):
#     # Parse table data string into rows and columns
#     rows = table_data_string.strip().split('\n')
#     table_data = [row.split('\t') for row in rows]

#     # Create a new workbook
#     workbook = Workbook()

#     # Get the active worksheet
#     sheet = workbook.active
#     sheet.title = 'Table Data'

#     # Write data to the worksheet
#     for row in table_data:
#         sheet.append(row)

#     workbook.save(os.path.join(app.config['UPLOAD_FOLDER'], excel_filename))
#     print(f"Table data has been successfully written to {excel_filename}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)
