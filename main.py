from io import StringIO
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
import glob
import re

PDF_FILES_DIR = ""

def get_cv_email( cv_path):
    pagenums = set()
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(cv_path, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = match.group(0)
    return email

pdfFiles = glob.glob(PDF_FILES_DIR+"*.pdf")


csvfile = open('emails.txt', 'w')
failed = open('failed.txt', 'w')

for file in pdfFiles:
    try:
        email = get_cv_email(cv_path=file)
        csvfile.write(email+"\n")
    except:
        print("extracting email failed for "+file)
        failed.write(file+"\n")


csvfile.flush()
csvfile.close()
failed.flush()
failed.close()