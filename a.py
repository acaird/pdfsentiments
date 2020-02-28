#!/usr/bin/env python3
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from io import StringIO


def analyze(pdffile):
    laparams = LAParams()
    laparams.all_texts = True
    outfp = sys.stdout
    sio = StringIO()
    # Open a PDF file.
    fp = open(pdffile, "rb")
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)
    device = TextConverter(rsrcmgr, sio, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)

    text = sio.getvalue()
    fp.close()
    device.close()
    sio.close()

    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)

    for key in sorted(scores):
        print("{0}: {1}, ".format(key, scores[key]), end="")

    print()


if __name__ == "__main__":

    pdffiles = [
        "examples/tb125heff-newusers.pdf",
        "examples/tb125menke-tug19.pdf",
        "examples/tb125reutenauer-xetex.pdf",
        "examples/tb125tug19-agm.pdf",
    ]

    for pdffile in pdffiles:
        print(pdffile)
        analyze(pdffile)
