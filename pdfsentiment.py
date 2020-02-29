#!/usr/bin/env python3

from PdfDocument.PdfDocument import PdfDocument

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
