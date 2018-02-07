import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from gooey import Gooey, GooeyParser




def extract(in_file, coords, searchString, out_file):
    with open(in_file, 'rb') as infp:
        reader = PdfFileReader(infp)
        writer = PdfFileWriter()
        #merger = PdfFileMerger()

        numPages = reader.getNumPages()
        print("document has %s pages." % numPages)

        for i in range(numPages):
            page = reader.getPage(i)
            pageText = page.extractText()
            if (pageText.find(searchString) != -1):
                page.mediaBox.lowerLeft = coords[:2]
                page.mediaBox.upperRight = coords[2:]
                writer.addPage(page)

        with open(out_file, 'wb') as outfp:
            writer.write(outfp)


def merge(in_file, out_file):
    with open(in_file, 'rb') as infp:
        reader = PdfFileReader(infp)
        writer = PdfFileWriter()
        #merger = PdfFileMerger()

        numPages = reader.getNumPages()
        print("document has %s pages." % numPages)

        #writer.addPage(reader.getPage(0))

        outpage = writer.addBlankPage(
            width=1,#reader.getPage(0).mediaBox.getWidth(),
            height=1,#reader.getPage(0).mediaBox.getHeight(),
        )


        for i in range(numPages):

            page = reader.getPage(i)
            page.mediaBox.lowerLeft
            spacing=35
            horOffset=160
            if i % 2 == 0:
                outpage.mergeRotatedTranslatedPage(page, 90, (i/2)*spacing, -(i/2)*spacing, expand=True)
            else:
                outpage.mergeRotatedTranslatedPage(page, 90, horOffset+(i/2)*spacing, horOffset-(i/2)*spacing, expand=True)
            #writer.getPage(0).mergeTranslatedPage(page.rotateClockwise(270),i*500,i*0, expand=True)
            #merger.append(page.rotateClockwise(270))

        

        
        with open(out_file, 'wb') as outfp:
            writer.write(outfp)

@Gooey
def main():
    parser = GooeyParser(description='Example with non-optional arguments')

    parser.add_argument('InputFile', action="store", widget="FileChooser", default="in.pdf")
    parser.add_argument('OutputFile', action="store", widget="FileChooser", default="out.pdf")
    parser.add_argument('x1', action="store", type=int, default=210)
    parser.add_argument('y1', action="store", type=int, default=50)
    parser.add_argument('x2', action="store", type=int, default=300)
    parser.add_argument('y2', action="store", type=int, default=380)
    parser.add_argument('--searchString', action="store", default="AP Article Id")

    print parser.parse_args()

    results = parser.parse_args()

    in_file = results.InputFile
    coords = [results.x1, results.y1, results.x2, results.y2]
    out_file = results.OutputFile

    extract(in_file, coords, results.searchString, out_file)
    merge(out_file, "merged.pdf")

if __name__ == '__main__':
    main()


