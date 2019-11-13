import os.path
import time

from core.download_links import LinksDownloader


class LinksUpdater:
    def __init__(self, p_root, p_path):
        self._root = p_root
        self._links = []
        self._links_local_file = p_path + "/resources/scihub_links.txt "

    def _local_file_need_update(self, force_update):
        if force_update:
            return True
        else:
            if os.path.isfile(self._links_local_file):
                sys_time = time.time()
                file_mtime = os.path.getmtime(self._links_local_file)
                if file_mtime + 259200 <= sys_time:  # If it is more than 3 days since last time the file was modified,
                    # then update the links in it.
                    return True
                else:
                    return False
            else:
                return True

    def _update_links(self):
        links_downloader = LinksDownloader(self._root, self._links_local_file)
        links_downloader.html_parser()

    def load_links(self, force_update=False):
        if self._local_file_need_update(force_update):
            self._update_links()
            print("SciHub links have updated.")

        self._links.clear()
        with open(self._links_local_file, "r") as fh:
            f_content = fh.readlines()
            for item in f_content:
                if len(item) > 1:
                    self._links.append(item.strip())

        return self._links

    def remove_invalid_links(self, p_invalid_links):
        with open(self._links_local_file, "w") as fh:
            for item in self._links:
                if item not in p_invalid_links:
                    # print(item)
                    fh.write(f'{item}\n')

        print("SciHub links have updated.")
        self.load_links()


if __name__ == '__main__':
    pass
