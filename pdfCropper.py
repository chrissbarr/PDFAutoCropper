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

        if(arguments.InputStartPage != None):
            first_page = arguments.FilterStartPage
        else:
            first_page = 0

        if(arguments.InputEndPage != None):
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


def merge(in_file, out_file, arguments):
    print("Beginning merge operation...")

    with open(in_file, 'rb') as infp:
        reader = PdfFileReader(infp)
        writer = PdfFileWriter()

        numPages = reader.getNumPages()

        outpage = writer.addBlankPage(
            width=1,
            height=1
        )

        yPadding=arguments.MergeXPadding
        xPadding=arguments.MergeYPadding
        rotation=arguments.Rotation
        yOffset=0
        xOffset=0

        for i in range(numPages):
            page = reader.getPage(i)

            if(rotation == 90 or rotation == 270):
                yBounds = page.mediaBox.getWidth()
                xBounds = page.mediaBox.getHeight()
            else:
                yBounds = page.mediaBox.getHeight()
                xBounds = page.mediaBox.getWidth()

            print("%s, %s" %(xBounds,yBounds))

            page.mediaBox.lowerLeft
            spacing=35
            horOffset=160

            if i % 2 == 0:
                outpage.mergeRotatedTranslatedPage(page, rotation, yOffset, -yOffset, expand=True)
                xOffset = xOffset + xBounds/2 + xPadding
            else:
                outpage.mergeRotatedTranslatedPage(page, rotation, xOffset+yOffset, xOffset-yOffset, expand=True)
                yOffset = yOffset + yBounds/2 + yPadding
                xOffset = 0

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

    ### Input Section
    input_group = parser.add_argument_group("File Input", "")
    input_group.add_argument('InputFile', metavar="Input File:", help="Select the PDF to be loaded", action="store", widget="FileChooser", default="in.pdf")
    input_page_group = parser.add_argument_group("", "", gooey_options={'show_border': True,'columns': 2})
    input_page_group.add_argument('--InputStartPage', metavar="Start Page", help="Pages before this will be discarded", action="store", type=int)
    input_page_group.add_argument('--InputEndPage', metavar="End Page", help="Pages after this will be discarded", action="store", type=int)

    ### Filter Section
    filter_group = parser.add_argument_group("Filter", "")
    filter_option_group = parser.add_argument_group("", "", gooey_options={'show_border': True,'columns': 4})
    filter_group.add_argument('--FilterString', metavar="Filter", help="Only keep pages containing this text (ignored if blank)", action="store", type=str)
    filter_option_group.add_argument('--FilterStringCaseIns', metavar="Case Insensitive", help="Should text search should ignore case", action="store_true")
    filter_option_group.add_argument('--FilterStringInvSearch', metavar="Invert Search", help="Include pages which do not match search", action="store_true")

    ### Crop Section
    crop_group = parser.add_argument_group("Crop", "")
    crop_option_group = parser.add_argument_group("", "", gooey_options={'show_border': True,'columns': 4})
    crop_group.add_argument('--CropEnable', metavar="Enable", help="Enable crop operation", action="store_true")
    crop_option_group.add_argument('--CropX1', metavar="X1", action="store", type=int, default='0')
    crop_option_group.add_argument('--CropY1', metavar="Y1", action="store", type=int, default='0')
    crop_option_group.add_argument('--CropX2', metavar="X2", action="store", type=int, default='100')
    crop_option_group.add_argument('--CropY2', metavar="Y2", action="store", type=int, default='100')
    crop_option_group.add_argument('--Rotation', metavar="Rotation (degrees)", action="store", type=int, default='0')

    ### Merge Section
    merge_group = parser.add_argument_group("Merge", "")
    merge_option_group = parser.add_argument_group("", "", gooey_options={'show_border': True,'columns': 4})
    merge_group.add_argument('--MergeEnable',  metavar="Enable", help="Enable merge operation", action="store_true")
    merge_option_group.add_argument('--MergeXPadding', metavar="Layout X Padding", action="store", type=int, default='0')
    merge_option_group.add_argument('--MergeYPadding', metavar="Layout Y Padding", action="store", type=int, default='0')

    ### Output Section
    output_group = parser.add_argument_group("Output", "")
    output_option_group = parser.add_argument_group("", "", gooey_options={'show_border': True,'columns': 2})
    output_group.add_argument('OutputFile', action="store", widget="FileChooser", default="out.pdf")
    output_option_group.add_argument('--OutputOpenFile', metavar="Open output file?", help="Open generated PDF when done", action="store_false", dest='leaveClosedOnFinish', default=True)
    output_option_group.add_argument('--OutputDeleteIntermed', metavar="Delete intermediary files?", help="Delete temporary files generated during process", action="store_false", dest='deleteTempFiles', default=True)

    print parser.parse_args()
    results = parser.parse_args()

    in_file = results.InputFile
    coords = [results.CropX1, results.CropY1, results.CropX2, results.CropY2]
    out_file = results.OutputFile

    filter(in_file, "filtered.pdf", results)

    crop("filtered.pdf", "extracted.pdf", coords)

    merge('extracted.pdf', out_file, results)

    if(results.leaveClosedOnFinish == False):
        if os.name == "nt":
            os.startfile(out_file)
        else:
            subprocess.call(("open", out_file))

if __name__ == '__main__':
    main()