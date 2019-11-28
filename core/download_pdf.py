import inspect
import json
import os.path
import re
# import subprocess
import wget
import sys

import requests
from bs4 import BeautifulSoup

from core.process_captcha import CaptchaProcessor
from core.update_links import LinksUpdater
import core.utils


class PdfDownloader:
    def __init__(self, p_root, p_path):
        self._links = []
        self._invalid_links = []
        self._failed_doc_links = []
        self._doc_links_local_map = {}
        self.links_updater = LinksUpdater(p_root, p_path)
        self.path = p_path

        core.utils.check_and_initialize_folder(p_path)
        self._doc_links_local_file = p_path + "/resources/doc_links.json "
        self._failed_doc_links_local_file = p_path + "/resources/failed_doc_links.txt "

    def _generate_doc_link(self, p_ex_link):
        if len(self._links) < 1:
            self._links = self.links_updater.load_links()
            if len(self._links) < 1:
                print("Error! No valid links found! Trying again...")
                self._links.clear()
                self._links = self.links_updater.load_links(True)
                if len(self._links) < 1:
                    print("Error! No valid links found! Check the base root!")
                    sys.exit(2)
                else:
                    print("Scihub links have been loaded.")
                    # print(f"Currently loaded links: {self._links}")
            else:
                print("Scihub links have been loaded.")
                # print(f"Currently loaded links: {self._links}")

        def has_href_and_onclick(tag):
            return tag.has_attr("href") and tag.has_attr("onclick") and tag["href"] == "#"

        for item in self._links:
            headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/77.0.3865.90 Safari/537.36",
                "content-type": "application/x-www-form-urlencoded",
                "cookie": "session=fe5492d337beb1516667b77084c30f04; __ddg_=672C970C9A11199D007A92AB555840D2F34B22AD; "
                          "refresh=1568704139.5742",
                "referer": item,
            }
            form_data = {
                "sci-hub-plugin-check": "",
                "request": p_ex_link,
            }

            try:
                results = requests.post(item, data=form_data, headers=headers)
            except requests.exceptions.RequestException:
                print(f"Link '{item}' is invalid.")
                self._invalid_links.append(item)
                continue
            else:
                soup = BeautifulSoup(results.text, "html.parser")
                try:
                    doc_link = re.findall(re.compile(r".*?=['\"]h?t?t?p?s?:?//(.+?)\?.+?['\"]"),
                                          soup.find_all(has_href_and_onclick)[0]["onclick"])[0]
                except IndexError:
                    print(f"Link '{item}' is invalid.")
                    self._invalid_links.append(item)
                    continue
                else:
                    print(f"Link '{item}' works!")
                    for pre_head in ["https://", "http://"]:
                        yield "".join([pre_head, doc_link])

    def _save_doc_links(self):
        if len(self._doc_links_local_map) > 0:
            with open(self._doc_links_local_file, "w") as fh:
                json.dump(self._doc_links_local_map, fh)
            print("Doc download links have been saved.")
        else:
            print("Doc download links have not been saved.")

    def _load_doc_links_lib(self):
        if os.path.isfile(self._doc_links_local_file):
            with open(self._doc_links_local_file, "r") as fh:
                for key, value in json.load(fh).items():
                    self._doc_links_local_map[key] = value
            return True
        else:
            return False

    def _perform_single_doc_download(self, p_doc_download_links):
        def has_name_img_and_id_captcha(tag):
            return tag.name == "img" and tag["id"] == "captcha"

        for link in p_doc_download_links:
            headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/77.0.3865.90 Safari/537.36",
                "referer": link,
            }

            req_session = requests.session()

            try:
                result_1 = req_session.get(link, headers=headers)
                soup = BeautifulSoup(result_1.text, "html.parser")
                img_result = soup.find_all(has_name_img_and_id_captcha)
            except Exception:
                # subprocess.run(["wget", link])
                _temp_file = wget.download(link)
                print(f"\nUse '{link}' to download to '{_temp_file}'!")
                return True
            else:
                if len(img_result) > 0:
                    captcha_processor = CaptchaProcessor(link, img_result[0]["src"], self.path)
                    image_name, captcha_code = captcha_processor.get_captcha_code()

                    for _count in range(5):
                        data = {
                            "id": image_name,
                            "answer": captcha_code
                        }
                        result_2 = req_session.post(link, data=data, headers=headers)
                        result_2.encoding = result_2.apparent_encoding

                        try:
                            result_temp = req_session.get(link, headers=headers)
                            soup_temp = BeautifulSoup(result_temp.text, "html.parser")
                            img_result_temp = soup_temp.find_all(has_name_img_and_id_captcha)
                        except Exception:
                            # subprocess.run(["wget", link])
                            _temp_file = wget.download(link)
                            print(f"\nUse '{link}' to download to '{_temp_file}'!")
                            return True
                        else:
                            if len(img_result_temp) > 0:
                                image_name, captcha_code = captcha_processor.get_captcha_code(img_result_temp[0]["src"])
                            else:
                                # subprocess.run(["wget", link])
                                _temp_file = wget.download(link)
                                print(f"\nUse '{link}' to download to '{_temp_file}'!")
                                return True

                        if _count == 4:
                            print(f"Times of downloading {link} have exceeded the maximum!")
                            return False
                else:
                    # subprocess.run(["wget", link])
                    _temp_file = wget.download(link)
                    print(f"\nUse '{link}' to download to '{_temp_file}'!")
                    return True

    def _get_add_download_doc_links(self, p_ex_link):
        if p_ex_link not in self._doc_links_local_map.keys():
            self._doc_links_local_map[p_ex_link] = []

        for item in self._generate_doc_link(p_ex_link):
            if item not in self._doc_links_local_map[p_ex_link]:
                self._doc_links_local_map[p_ex_link].append(item)

        if not self._perform_single_doc_download(self._doc_links_local_map[p_ex_link]):
            print(f"{p_ex_link} downloading status: failed! The potential links are: "
                  f"{self._doc_links_local_map[p_ex_link]}")
            self._failed_doc_links.append(p_ex_link)
        else:
            print(f"'{p_ex_link}' downloading status: Succeeded!!")

    def _in_or_out_lib(self, p_ex_link):
        if p_ex_link in self._doc_links_local_map.keys():
            if not self._perform_single_doc_download(self._doc_links_local_map[p_ex_link]):
                self._get_add_download_doc_links(p_ex_link)
            else:
                print(f"'{p_ex_link}' downloading status: Succeeded!!")
        else:
            self._get_add_download_doc_links(p_ex_link)

    def download_from_link(self, p_ex_link):
        if len(self._doc_links_local_map) < 1:
            if self._load_doc_links_lib():
                self._in_or_out_lib(p_ex_link)
            else:
                self._get_add_download_doc_links(p_ex_link)
        else:
            self._in_or_out_lib(p_ex_link)

        if len(self._invalid_links) > 0:
            self._links = self.links_updater.remove_invalid_links(self._invalid_links)

        if inspect.stack()[1].function != "download_from_file":
            self._save_doc_links()

    def download_from_file(self, ex_file):
        try:
            fh = open(ex_file, "r")
        except FileNotFoundError:
            print("File does not exist!")
            sys.exit(2)
        else:
            f_contents = fh.readlines()
            for item in f_contents:
                if len(item) > 1:
                    self.download_from_link(item.strip())

            fh.close()

            self._save_doc_links()

            if len(self._failed_doc_links) > 0:
                with open(self._failed_doc_links_local_file, "w") as fh:
                    for item in self._failed_doc_links:
                        fh.write(f'{item}\n')
                print(f"Failed doc items have been saved to {os.path.abspath(self._failed_doc_links_local_file)}")


if __name__ == "__main__":
    root = "https://whereisscihub.now.sh/"
    pdf_downloader = PdfDownloader(root)

