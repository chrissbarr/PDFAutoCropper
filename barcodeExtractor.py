import sys
import os
import subprocess
from PyPDF2 import PdfFileReader, PdfFileWriter
from gooey import Gooey, GooeyParser

nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
sys.stdout = nonbuffered_stdout

def filter(in_file, out_file, arguments):
    print("Beginning filter operation...")

    with open(in_file, 'rb') as infp:
        reader = PdfFileReader(infp)
        writer = PdfFileWriter()
        numPages = reader.getNumPages()
        print("Document has %s pages." % numPages)

        if(arguments.FilterStartPage != None):
            first_page = arguments.FilterStartPage
        else:
            first_page = 0

        if(arguments.FilterEndPage != None):
            last_page = arguments.FilterEndPage
        else:
            last_page = numPages

        print("Filtering on pages %s to %s" %(first_page, last_page))

        for i in range(first_page, last_page):

            page = reader.getPage(i)
            if(arguments.FilterString != None):
                
                pageText = page.extractText()

                if(arguments.FilterStringCaseIns==True):
                    pageText = pageText.lower()
                    arguments.FilterString = arguments.FilterString.lower()

                if (pageText.find(arguments.FilterString) != -1):
                    print("Page %s contains filter string %s..." % (i, arguments.FilterString))
                else:
                    continue

            writer.addPage(page)

        with open(out_file, 'wb') as outfp:
           writer.write(outfp)

        print("Filtering complete, filtered output written to '%s'" % out_file)


def crop(in_file, out_file, coords):
    print("Beginning crop operation...")

    with open(in_file, 'rb') as infp:
        reader = PdfFileReader(infp)
        writer = PdfFileWriter()

        numPages = reader.getNumPages()

        for i in range(numPages):
            page = reader.getPage(i)
            page.mediaBox.lowerLeft = coords[:2]
            page.mediaBox.upperRight = coords[2:]
            writer.addPage(page)

        with open(out_file, 'wb') as outfp:
           writer.write(outfp)

        print("Cropping complete, cropped output written to '%s'" % out_file)


def merge(in_file, out_file, rotation):
    print("Beginning merge operation...")

    with open(in_file, 'rb') as infp:
        reader = PdfFileReader(infp)
        writer = PdfFileWriter()

        numPages = reader.getNumPages()

        outpage = writer.addBlankPage(
            width=1,
            height=1
        )

        for i in range(numPages):
            page = reader.getPage(i)

            page.mediaBox.lowerLeft
            spacing=35
            horOffset=160
            if i % 2 == 0:
                outpage.mergeRotatedTranslatedPage(page, rotation, (i/2)*spacing, -(i/2)*spacing, expand=True)
            else:
                outpage.mergeRotatedTranslatedPage(page, rotation, horOffset+(i/2)*spacing, horOffset-(i/2)*spacing, expand=True)

        with open(out_file, 'wb') as outfp:
           writer.write(outfp)

        print("Merge complete, merged output written to '%s'" % out_file)

@Gooey (
    program_name='PDF AutoCropper',
    program_description='Automatically crop and collate PDF pages',
    dump_build_config=True,  # Dump the JSON Gooey uses to configure itself
    load_build_config=None    # Loads a JSON Gooey-generated configuration
    )
def main():
    parser = GooeyParser()

    input_group = parser.add_argument_group(
        "", 
        ""
    )

    input_group.add_argument('InputFile', metavar="Input File:", help="Select the PDF to be loaded", action="store", widget="FileChooser", default="in.pdf")

    filter_group = parser.add_argument_group(
        "Filter", 
        ""
    )
    filter_group.add_argument('--FilterStartPage',      metavar="Start Page",       help="Pages before this will be discarded",     action="store",         type=int)
    filter_group.add_argument('--FilterEndPage',        metavar="End Page",         help="Pages after this will be discarded",      action="store",         type=int)
    filter_group.add_argument('--FilterString',         metavar="Filter",           help="Only keep pages containing this text",    action="store",         type=str)
    filter_group.add_argument('--FilterStringCaseIns',  metavar="Case Insensitive", help="Should text search should ignore case",   action="store_true")

    proc_group = parser.add_argument_group(
        "Crop", 
        ""
    )
    proc_group.add_argument('x1', action="store", type=int, default='0')
    proc_group.add_argument('y1', action="store", type=int, default='0')
    proc_group.add_argument('x2', action="store", type=int, default='100')
    proc_group.add_argument('y2', action="store", type=int, default='100')
    proc_group.add_argument('rotation', metavar="Rotation (degrees)", action="store", type=int, default='0')

    output_group = parser.add_argument_group(
        "Output", 
        ""
    )
    output_group.add_argument('OutputFile', action="store", widget="FileChooser", default="out.pdf")
    output_group.add_argument('--OpenOutput', metavar="Open output file?", help="Open generated PDF when done", action="store_false", dest='leaveClosedOnFinish', default=True)

    print parser.parse_args()

    results = parser.parse_args()

    in_file = results.InputFile
    coords = [results.x1, results.y1, results.x2, results.y2]
    out_file = results.OutputFile

    filter(in_file, "filtered.pdf", results)

    crop("filtered.pdf", "extracted.pdf", coords)

    merge('extracted.pdf', out_file, results.rotation)

    if(results.leaveClosedOnFinish == False):
        if os.name == "nt":
            os.startfile(out_file)
        else:
            subprocess.call(("open", out_file))

if __name__ == '__main__':
    main()