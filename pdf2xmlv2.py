import PyPDF2
import docx
import pytesseract
from PIL import Image
import re
import os
import tkinter as tk
from tkinter import filedialog

def pdf_to_xml(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    xml_text = '<document>\n'
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        xml_text += '<page>\n'
        xml_text += page_text
        xml_text += '</page>\n'
    xml_text += '</document>'
    return xml_text

def docx_to_xml(file_path):
    doc = docx.Document(file_path)
    xml_text = '<document>\n'
    for para in doc.paragraphs:
        xml_text += '<paragraph>\n'
        xml_text += para.text
        xml_text += '</paragraph>\n'
    xml_text += '</document>'
    return xml_text

def image_to_text(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    text = re.sub(r'[^\x00-\x7F]+', '', text) # remove non-ascii characters
    return text

def file_to_xml(file_path):
    if file_path.endswith('.pdf'):
        xml_text = pdf_to_xml(file_path)
    elif file_path.endswith('.docx'):
        xml_text = docx_to_xml(file_path)
    elif file_path.endswith('.jpg') or file_path.endswith('.png'):
        text = image_to_text(file_path)
        xml_text = '<document>\n'
        xml_text += '<page>\n'
        xml_text += text
        xml_text += '</page>\n'
        xml_text += '</document>'
    else:
        return None

    # Save XML text to file
    xml_file_path = os.path.splitext(file_path)[0] + '.xml'
    with open(xml_file_path, 'w') as xml_file:
        xml_file.write(xml_text)

    return xml_text

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        xml_text = file_to_xml(file_path)
        if xml_text:
            success_label.config(text='Conversion successful!')
        else:
            success_label.config(text='Invalid file type')

root = tk.Tk()
root.title('PDF/DOCX to XML Converter')

upload_button = tk.Button(root, text='Upload File', command=browse_file)
upload_button.pack(pady=20)

success_label = tk.Label(root, text='')
success_label.pack()

root.mainloop()