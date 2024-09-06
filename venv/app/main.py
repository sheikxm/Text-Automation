# app/main.py
from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import os

# Specify the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def append_text(output_file_path, index, filename, text):
    with open(output_file_path, 'a') as file:
        file.write(f"\n{index}. Text from {filename}:\n{text}\n\n")


@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None

    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        append_text_checked = request.form.get('appendText') == 'on'

        if uploaded_files:
            if not os.path.exists('app/uploads'):
                os.makedirs('app/uploads')

            output_file_path = 'app/output.txt'

            for index, uploaded_file in enumerate(uploaded_files, start=1):
                image_path = 'app/uploads/' + uploaded_file.filename
                uploaded_file.save(image_path)

                text = extract_text_from_image(image_path)
                extracted_text = extracted_text + '\n' + text if extracted_text else text

                append_text(output_file_path, index, uploaded_file.filename, text)

    return render_template('index.html', message=None, extracted_text=extracted_text)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
