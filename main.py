import getopt
import sys
import os

from core.download_pdf import PdfDownloader

help_msg = """usage: 

To download a paper using doi code or link or title (if containing spaces, please quote the string):
python3 your_file.py -l your_scihub_link
or:
python3 your_file.py --link=your_scihub_link

To download a bunch of papers using doi codes or links in a txt document:
python3 your_file.py -f path_to_your_txt_doc
or:
python3 your_file.py --file=path_to_your_txt_doc"""

root = "https://whereisscihub.now.sh/"


def main(argv, path):
    pdf_downloader = PdfDownloader(root, path)

    try:
        opts, args = getopt.getopt(argv, "hl:f:", ["link=", "file="])
    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == "-h":
                print(help_msg)
                sys.exit()
            if opt in ("-l", "--link"):
                pdf_downloader.download_from_link(arg)
            if opt in ("-f", "--file"):
                pdf_downloader.download_from_file(arg)


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    main(sys.argv[1:], dir_path)
