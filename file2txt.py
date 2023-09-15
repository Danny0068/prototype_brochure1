
import docx2txt
import PyPDF2

def convert_pdf_to_text(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def convert_docx_to_text(docx_file):
    text = docx2txt.process(docx_file)
    return text
