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

total_pages = 100
folder = '/Volumes/mac移动'


class KpopDownload:
    def __init__(self, name):
        self.name = name
        self.create_dir()
        self.get_download_link()

    def create_dir(self):
        if not os.path.exists(f'{folder}/{self.name}'):
            os.mkdir(f'{folder}/{self.name}')

    # noinspection PyMethodMayBeStatic
    def download_one_picture(self, link: str):
        pic_content = requests.get(link, headers=headers)
        pic_name = link.split('.')[1].split('/')[-1]
        with open(f"/Volumes/mac移动/{self.name}/{pic_name}.jpeg", "wb") as file:
            file.write(pic_content.content)

    def get_download_link(self):
        ex = '<a href="(.*?)" class="cell" aria-label="album">'  # 每个人下面图片链接的正则
        for i in range(1, total_pages + 1):
            response = requests.post(r"https://kpopping.com/profiles/idol/{}/latest-pictures/{}".format(self.name, i))
            if response.status_code != 200:
                print(f"第:{i}页,停止了下载,因为只有这么多页")
                return
            idol_img_json = json.loads(response.text)
            image_list = re.findall(ex, idol_img_json['content'])  # 找到每页的12个链接
            image_list_link = ['https://kpopping.com' + x for x in image_list]
            print(len(image_list_link), "单次下载长度", f"第{i}页")
            with concurrent.futures.ThreadPoolExecutor() as pool2:
                pool2.map(self.download_all_picture, image_list_link)

    def download_all_picture(self, link):
        d_link = []
        r = requests.get(link, headers=headers).text
        one_picture_ex = '<a href="/documents/(.*?)" data'  # 每一页下所有图片的正则
        p = re.findall(one_picture_ex, r)
        for i in p:
            d_link.append("https://kpopping.com/documents/" + i)
        with concurrent.futures.ThreadPoolExecutor() as download_pool:
            download_pool.map(self.download_one_picture, d_link)


if __name__ == "__main__":
    # idol_name = ["Wonyoung", "Karina2", "Leeseo", "Yujin3", "Miyeon", "IU"，'Gaeul5']
    idol_name = ['Liz2']
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(KpopDownload, idol_name)
    print("下载完成")
