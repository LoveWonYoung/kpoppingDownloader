import json
import re

import requests

# test
'''
405 Method Not Allowed
'''

r = r"https://kpopping.com/profiles/idol/Karina2/latest-pictures/1000"

# resp = requests.post(r)
# print(resp.status_code)

# j = json.loads(resp.text)
# print(j['content'])
'''
https://kpopping.com/kpics/240710-KARINA-Instagram-Update-with-GISELLE

下载链接 ；https://kpopping.com/kpics/download/240709-KARINA-Instagram-Update
'''


def get_download_link():
    ex = '<a href="(.*?)" class="cell" aria-label="album">'
    ret = []
    page_count = 0
    for i in range(10000):
        response = requests.post(r"https://kpopping.com/profiles/idol/Karina2/latest-pictures/{}".format(i))
        if response.status_code != 200:
            return
        idol_img_json = json.loads(response.text)

        image_list = re.findall(ex, idol_img_json['content'])
        ret += image_list
        print(page_count)
        page_count += 1
    print(page_count)
    return ret


def downloader():
    pass


if __name__ == "__main__":
    get_download_link()
