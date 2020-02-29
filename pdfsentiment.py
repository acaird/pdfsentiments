#!/usr/bin/env python3

import argparse
from PdfDocument.PdfDocument import PdfDocument


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file or files to process", nargs="+")

    return parser.parse_args()


if __name__ == "__main__":

    args = process_args()

    for pdffile in args.file:
        pdf = PdfDocument(pdffile)
        print(pdffile, pdf.creation_date)

        pdf.sentiment()
        print(pdf.scores)
