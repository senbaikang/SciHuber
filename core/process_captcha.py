import json
import os.path
import re
import subprocess
import time

import requests
from PIL import Image
from io import BytesIO


class CaptchaProcessor:
    def __init__(self, p_doc_link, p_img_link, p_path):
        self._doc_link = p_doc_link
        self._img_link = p_img_link
        self._last_img_name = ""
        self._img_name_code_map = {}
        self._captcha_local_file = p_path + "/resources/captcha_codes.json "
        self._temp_img_local_file = p_path + "/resources/temp_img"

    def _load_img_codes_lib(self):
        if len(self._img_name_code_map) < 1:
            if os.path.isfile(self._captcha_local_file):
                with open(self._captcha_local_file) as fh:
                    for key, value in json.load(fh).items():
                        self._img_name_code_map[key] = value
                return True
            else:
                return False
        else:
            return True

    def _get_code_from_img(self, p_base_url, p_img_format):
        img = Image.open(BytesIO(requests.get("".join([p_base_url, self._img_link])).content))
        img_path = "".join([self._temp_img_local_file, p_img_format])
        img.save(img_path)

        viewer = subprocess.Popen(['feh', img_path])
        time.sleep(4)
        viewer.terminate()
        viewer.kill()

        code = input("Please input the code: ")

        subprocess.run(["rm", img_path])

        return code

    def _save_img_codes(self):
        if len(self._img_name_code_map) > 0:
            with open(self._captcha_local_file, "w") as fh:
                json.dump(self._img_name_code_map, fh)
            print("Captcha codes have been saved.")
        else:
            print("Captcha codes have not been saved.")

    def _consensus_code(self, p_base_url, p_img_format):
        while True:
            print("Input the code in the image twice for a consensus.")
            code = set()
            for _ in range(2):
                code.add(self._get_code_from_img(p_base_url, p_img_format))
            if len(code) == 1:
                for item in code:
                    return item

    def get_captcha_code(self, p_img_link=None):
        if p_img_link is not None:
            self._img_link = p_img_link

        base_url = re.findall(re.compile(r"(https?://.+?)/"), self._doc_link)[0]
        img_re_result = re.findall(re.compile(r"/img/(.+?)(\..+)"), self._img_link)
        img_name = img_re_result[0][0]
        img_format = img_re_result[0][1]

        if self._load_img_codes_lib():
            if img_name == self._last_img_name:
                code = self._consensus_code(base_url, img_format)
                self._img_name_code_map[img_name] = code
            else:
                if img_name in self._img_name_code_map.keys():
                    code = self._img_name_code_map[img_name]
                else:
                    code = self._get_code_from_img(base_url, img_format)
                    self._img_name_code_map[img_name] = code
                self._last_img_name = img_name
        else:
            code = self._get_code_from_img(base_url, img_format)
            self._img_name_code_map[img_name] = code
            self._last_img_name = img_name

        self._save_img_codes()

        return img_name, code


if __name__ == '__main__':
    pass
