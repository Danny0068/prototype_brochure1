import os
from config import KEY
import openai
import base64
from file2txt import convert_pdf_to_text, convert_docx_to_text
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

# Set your OpenAI API key
openai_api_key = KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', text_input='', generated_text='', processed_filenames=[], extracted_text='', paragraphs=[], image='')

    elif request.method == 'POST':
        text_input = request.form.get('text_input')
        size = request.form.get('image_size')
        file_type = request.form.get('file_type')

        # Process PDF and DOCX files
        file_upload = request.files.get('file_upload')

        extracted_text = ""
        processed_filenames = []  # Initialize the list to store processed file names

        if file_upload:
            if file_type == "pdf":
                extracted_text = convert_pdf_to_text(file_upload)
            elif file_type == "docx":
                extracted_text = convert_docx_to_text(file_upload)
            processed_filenames.append(file_upload.filename)  # Add file name

        # Generate image
        try:
            response = generate_image(text_input, size)

            if response:
                image_data = base64.b64decode(response['image'])

                # Generate text
                generated_text = generate_text(extracted_text)

                return render_template('index.html', text_input=text_input, generated_text=generated_text, processed_filenames=processed_filenames, extracted_text=extracted_text, paragraphs=[], image=image_data)
            else:
                return render_template('index.html', text_input=text_input, generated_text='', processed_filenames=[], extracted_text=extracted_text, paragraphs=[], image='')

        except Exception as e:
            return render_template('index.html', text_input=text_input, generated_text='your genrated will be shown here ', processed_filenames=["please","write","something"], extracted_text=extracted_text, paragraphs=[], image='')

# Function to generate image (Replace with your OpenAI image generation code)
def generate_image(text, size):
    openai.api_key = os.environ.get(KEY)

    response = openai.Image.create(
        prompt=text,
        n=1,
        size=size,
        response_format="b64_json",
    )

    return response

# Function to generate text using OpenAI GPT-3
def generate_text(input_text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f" write a paragraph for  the following {input_text}",
        max_tokens=50  # Adjust the max_tokens as needed
    )

    generated_text = response.choices[0].text
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)

