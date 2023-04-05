import PyPDF2
import docx
import pytesseract
from PIL import Image
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

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
    elif file_path.endswith('.xml'):
        with open(file_path, 'r') as xml_file:
            xml_text = xml_file.read()
    else:
        return None

    # Save XML text to file
    if not file_path.endswith('.xml'):
        xml_file_path = os.path.splitext(file_path)[0] + '.xml'
        with open(xml_file_path, 'w') as xml_file:
            xml_file.write(xml_text)
    else:
        xml_file_path = file_path

    return xml_text, xml_file_path

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        xml_text, xml_file_path = file_to_xml(file_path)
        if xml_text:
            success_label.config(text='Conversion successful!')
            show_xml_editor(xml_text, xml_file_path)

def open_xml():
    file_path = filedialog.askopenfilename(filetypes=[('XML Files', '*.xml')])
    if file_path:
        xml_text, xml_file_path = file_to_xml(file_path)
        if xml_text:
            show_xml_editor(xml_text, xml_file_path)

def show_xml_editor(xml_text, file_path):
    def save_xml():
        modified_xml_text = xml_editor.get('1.0', 'end')
        with open(file_path, 'w') as xml_file:
            xml_file.write(modified_xml_text)
        messagebox.showinfo('Save', 'XML file saved successfully')

    xml_editor_window = tk.Toplevel(root)
    xml_editor_window.title('XML Editor')

    xml_editor = scrolledtext.ScrolledText(xml_editor_window, width=80, height=30)
    xml_editor.pack(padx=10, pady=10)
    xml_editor.insert('1.0', xml_text)

    save_button = tk.Button(xml_editor_window, text='Save', command=save_xml)
    save_button.pack(pady=10)

root = tk.Tk()
root.title('PDF/DOCX to XML Converter')

upload_button = tk.Button(root, text='Upload File', command=browse_file)
upload_button.pack(pady=20)

open_button = tk.Button(root, text='Open XML', command=open_xml)
open_button.pack(pady=10)

success_label = tk.Label(root, text='')
success_label.pack()

root.mainloop()