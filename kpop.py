import concurrent.futures
import json
import os.path
import re

import requests

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 '
        'Safari/537.36'
}


class KpopDownload:
    def __init__(self, name):
        self.name = name
        self.create_dir()
        self.get_download_link()

    def create_dir(self):
        if not os.path.exists(f'/Volumes/mac移动/{self.name}'):
            os.mkdir(f'/Volumes/mac移动/{self.name}')

    # noinspection PyMethodMayBeStatic
    def download_one_pic(self, link: str):
        pic_content = requests.get(link, headers=headers)
        pic_name = link.split('.')[1].split('/')[-1]
        with open(f"/Volumes/mac移动/{self.name}/{pic_name}.jpeg", "wb") as file:
            file.write(pic_content.content)

    def get_download_link(self):
        ex = '<a href="(.*?)" class="cell" aria-label="album">'

        for i in range(2):
            response = requests.post(r"https://kpopping.com/profiles/idol/{}/latest-pictures/{}".format(self.name, i))
            if response.status_code != 200:
                print(f"page:{i}停止了下载")
                return
            idol_img_json = json.loads(response.text)
            image_list = re.findall(ex, idol_img_json['content'])  # 找到12个链接
            image_list_link = ['https://kpopping.com' + x for x in image_list]
            print(len(image_list_link), "单次下载长度", f"第{i}页")
            with concurrent.futures.ThreadPoolExecutor() as pool:
                pool.map(self.get_pic_link, image_list_link)

    def get_pic_link(self, link):
        d_link = []
        r = requests.get(link, headers=headers).text
        ex = '<a href="/documents/(.*?)" data'
        p = re.findall(ex, r)
        for i in p:
            d_link.append("https://kpopping.com/documents/" + i)
        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.map(self.download_one_pic, d_link)


if __name__ == "__main__":
    idol_name = ["Wonyoung", "Karina2", "Leeseo", "Yujin3", "Miyeon", "IU"]
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(KpopDownload, idol_name)
    print("下载完成")
