import os
import re
import sys

import urllib3
from bs4 import BeautifulSoup


class LinksDownloader:
    def __init__(self, p_root, p_local_file):
        self._root = p_root
        self._links = []
        self._content = ""
        self._links_local_file = p_local_file

    def _get_content(self):
        http = urllib3.PoolManager()
        try:
            r = http.request("GET", self._root)
        except ConnectionError:
            print("Could not connect. The default root link is invalid.")
            sys.exit(2)
        else:
            self._content = r.data.decode()

    def _write_to_file(self):
        if len(self._links) == 0:
            print("No available links found!")
            sys.exit(0)
        else:
            with open(self._links_local_file, "w") as fh:
                for item in self._links:
                    fh.write(f'{item}\n')

    def html_parser(self):
        self._get_content()
        soup = BeautifulSoup(self._content, "html.parser")

        reg_expr = re.compile(r'https?://.+')
        for item in soup.find_all("a"):
            try:
                item['title']
            except KeyError:
                if re.search(reg_expr, str(item.string)):
                    self._links.append(str(item.string))

        self._write_to_file()


if __name__ == "__main__":
    root = "https://whereisscihub.now.sh/"
    local_file = os.getcwd() + "/resources/scihub_links.txt"
    links_downloader = LinksDownloader(root, local_file)
    links_downloader.html_parser()
