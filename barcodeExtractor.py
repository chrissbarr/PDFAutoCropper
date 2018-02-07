import sys
from PyPDF2 import PdfFileReader, PdfFileWriter


def extract(in_file, coords, out_file):
    with open(in_file, 'rb') as infp:
        reader = PdfFileReader(infp)
        writer = PdfFileWriter()
        #merger = PdfFileMerger()

        numPages = reader.getNumPages()
        print("document has %s pages." % numPages)


        for j in range(2):
            for i in range(numPages):
                page = reader.getPage(i)
                pageText = page.extractText()
                if (pageText.find("AP Article Id") != -1):
                    #print(pageText)
                    page.mediaBox.lowerLeft = coords[:2]
                    page.mediaBox.upperRight = coords[2:]
                    writer.addPage(page)#.rotateClockwise(270))
                #writer.getPage(0).mergeTranslatedPage(page.rotateClockwise(270),i*500,i*0, expand=True)
                #merger.append(page.rotateClockwise(270))

        

        
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


if __name__ == '__main__':
    in_file = sys.argv[1]
    coords = [int(i) for i in sys.argv[2:6]]
    out_file = sys.argv[6]

    extract(in_file, coords, out_file)
    merge(out_file, "merged.pdf")
