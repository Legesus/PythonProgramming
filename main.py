import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
import docx2txt
import PyPDF2

def replace_ascii_codes(text):
    ascii_codes = {"&#8217;": "'", "&#8221;": '"', "&#8220;": '"'}
    for code, symbol in ascii_codes.items():
        if code != "&amp;amp;":
            text = text.replace(code, symbol)
    return text

def generate_corrected_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as xml_file:
        xml_contents = xml_file.read()
    corrected_contents = replace_ascii_codes(xml_contents)
    corrected_file_path = os.path.splitext(file_path)[0] + '_corrected.xml'
    with open(corrected_file_path, 'w', encoding='utf-8') as corrected_file:
        corrected_file.write(corrected_contents)
    os.remove(file_path)
    os.rename(corrected_file_path, file_path)
    os.chmod(file_path, 0o777)
    os.chmod(corrected_file_path, 0o777)

def convert_pdf_to_xml(file_path):
    # Open the PDF file in read-binary mode
    with open(file_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Create a new XML element
        root = ET.Element('document')

        # Loop through each page of the PDF file
        for page_num in range(pdf_reader.getNumPages()):
            # Get the text of the page
            page = pdf_reader.getPage(page_num)
            page_text = page.extractText()

            # Create a new XML element for the page
            page_element = ET.SubElement(root, 'page')
            page_element.set('number', str(page_num + 1))

            # Add the text to the page element
            page_element.text = page_text

        # Create a new XML file
        xml_file_path = os.path.splitext(file_path)[0] + '.xml'
        ET.ElementTree(root).write(xml_file_path)

        # Generate corrected XML file
        generate_corrected_xml(xml_file_path)

        # Show a message in the console
        print(f"File converted to XML file:\n{xml_file_path}")

def convert_docx_to_xml(file_path):
    root = ET.Element('document')
    docx_text = docx2txt.process(file_path)
    pages = docx_text.split('\f')
    for page_num, page_text in enumerate(pages):
        page_element = ET.SubElement(root, 'page')
        page_element.set('number', str(page_num + 1))
        page_element.text = page_text
    xml_file_path = os.path.splitext(file_path)[0] + '.xml'
    ET.ElementTree(root).write(xml_file_path)
    generate_corrected_xml(xml_file_path)
    # Show a message in the console
    print(f"File converted to XML file:\n{xml_file_path}")

def handle_select():
    file_type = toggle_button['text'].lower()
    file_path = filedialog.askopenfilename(filetypes=[(f"{file_type.upper()} files", f"*.{file_type}")])
    if file_path:
        if file_type == 'pdf':
            convert_pdf_to_xml(file_path)
        elif file_type == 'docx':
            convert_docx_to_xml(file_path)

def handle_toggle():
    if file_type.get() == "pdf":
        file_type.set("docx")
        toggle_button.config(text="Convert to PDF")
        label.config(text="Click the button to select a DOCX file")
    else:
        file_type.set("pdf")
        toggle_button.config(text="Convert to DOCX")
        label.config(text="Click the button to select a PDF file")

window = tk.Tk()
window.title("File Converter")

file_type = tk.StringVar(value="pdf")
label = ttk.Label(window, text="Click the button to select a PDF file")
label.pack(pady=10)

button = ttk.Button(window, text="Select a file", command=handle_select)
button.pack(pady=10)

toggle_button = ttk.Button(window, text="Convert to DOCX", command=handle_toggle)
toggle_button.pack(pady=10)

window.mainloop()