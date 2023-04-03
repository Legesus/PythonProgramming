import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pytesseract
import docx
import docx2txt
import PyPDF2
import xml.etree.ElementTree as ET

# Create a new window
window = tk.Tk()
window.title("PDF to XML Converter")

# Create a label widget
label = ttk.Label(window, text="Click the button to select a PDF file")
label.pack(padx=50, pady=20)

# Create a function to handle file selection
def handle_select():
    # Show a file dialog to select a PDF file
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    # Check if a file was selected
    if file_path:
        # Open the PDF file
        with open(file_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Create a new Word document
            docx_file_path = os.path.splitext(file_path)[0] + '.docx'
            doc = docx.Document()

            # Loop through each page of the PDF file and add the text to the Word document
            for page_num in range(len(pdf_reader.pages)):
                # Get the page object
                page = pdf_reader.pages[page_num]

                # Extract the text from the page
                text = page.extract_text()

                # Add the text to the Word document
                if text:
                    if page_num > 0:
                        doc.add_page_break()
                    doc.add_paragraph(text)

            # Save the Word document
            doc.save(docx_file_path)

            # Create a new XML element
            root = ET.Element('document')

            # Get the text of the Word document
            docx_text = docx2txt.process(docx_file_path)

            # Split the text into pages
            pages = docx_text.split('\f')

            # Loop through each page of the Word document
            for page_num, page_text in enumerate(pages):
                # Create a new XML element for the page
                page_element = ET.SubElement(root, 'page')
                page_element.set('number', str(page_num + 1))

                # Add the text to the page element
                page_element.text = page_text

            # Create a new XML file
            xml_file_path = os.path.splitext(file_path)[0] + '.xml'
            ET.ElementTree(root).write(xml_file_path)

            # Show a message box with the path of the XML file
            messagebox.showinfo("Conversion Complete", f"PDF file converted to XML file:\n{xml_file_path}")

# Create a button to select a file
button = ttk.Button(window, text="Select a PDF file", command=handle_select)
button.pack(pady=10)

# Run the main event loop
window.mainloop()