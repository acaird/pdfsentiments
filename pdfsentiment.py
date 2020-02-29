#!/usr/bin/env python3

import argparse
from PdfDocument.PdfDocument import PdfDocument


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="PDF file or files to process", nargs="+", required=True
    )

    return parser.parse_args()


if __name__ == "__main__":

    args = process_args()

    for pdffile in args.file:
        pdf = PdfDocument(pdffile)
        print(pdffile, pdf.creation_date)

        pdf.sentiment()
        print(pdf.scores)
