#!/usr/bin/env python3
import sys
from datetime import datetime
from io import StringIO
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser

"""Use the laziest possible sentiment analysis on PDF files

I just Googled some stuff.

Plus, I read this:
   https://monkeylearn.com/sentiment-analysis/
but didn't really pay attention to it
"""


class PdfDocument:
    """A PdfDocument Object

    Contains the text and PDF document information and offers a
    sentiment method that runs a simplistic sentiment analysis on the
    text of the PDF file

    """

    def __init__(self, pdffile):
        """Create the PDF Document object

        Reads a PDF file and turns it into a text string and extracts
        some document info

        """
        self.scores = {}
        laparams = LAParams()
        laparams.all_texts = True
        sio = StringIO()

        fp = open(pdffile, "rb")
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        document = PDFDocument(PDFParser(fp))

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

        self.pdffile_text = sio.getvalue()
        self.info = document.info
        # 20190915234815+02'00'
        self.creation_date = datetime.strptime(
            str(self.info[0]["CreationDate"]).split("+")[0].split(":")[1],
            "%Y%m%d%H%M%S",
        )
        fp.close()
        device.close()
        sio.close()

    def sentiment(self):
        """Run a simplistic sentiment analysis

        Use the NLTK VADER (https://github.com/cjhutto/vaderSentiment)
        library to get polarity scores

        From
        https://github.com/cjhutto/vaderSentiment#about-the-scoring

        > The compound score is computed by summing the valence scores
          of each word in the lexicon, adjusted according to the
          rules, and then normalized to be between -1 (most extreme
          negative) and +1 (most extreme positive). This is the most
          useful metric if you want a single unidimensional measure of
          sentiment for a given sentence. Calling it a 'normalized,
          weighted composite score' is accurate.

        > The pos, neu, and neg scores are ratios for proportions of
          text that fall in each category (so these should all add up
          to be 1... or close to it with float operation). These are
          the most useful metrics if you want multidimensional
          measures of sentiment for a given sentence.

        """
        sid = SentimentIntensityAnalyzer()
        self.scores = sid.polarity_scores(self.pdffile_text)


if __name__ == "__main__":

    pdffiles = [
        "examples/tb125heff-newusers.pdf",
        "examples/tb125menke-tug19.pdf",
        "examples/tb125reutenauer-xetex.pdf",
        "examples/tb125tug19-agm.pdf",
    ]

    for pdffile in pdffiles:
        pdf = PdfDocument(pdffile)
        print(pdffile, pdf.creation_date)

        pdf.sentiment()
        print(pdf.scores)
