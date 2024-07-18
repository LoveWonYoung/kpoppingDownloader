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

name = "Leeseo"

if not os.path.exists(f'/Users/wonyoung/Desktop/{name}'):
    os.mkdir(f'/Users/wonyoung/Desktop/{name}')


# https://kpopping.com/profiles/idol/Yujin3
def download_one_pic(link: str):
    pic_content = requests.get(link, headers=headers)
    pic_name = link.split('.')[1].split('/')[-1]
    with open(f"/Users/wonyoung/Desktop/{name}/{pic_name}.jpeg", "wb") as file:
        file.write(pic_content.content)


def get_download_link():
    ex = '<a href="(.*?)" class="cell" aria-label="album">'

    for i in range(1000):
        response = requests.post(r"https://kpopping.com/profiles/idol/{}/latest-pictures/{}".format(name, i))
        if response.status_code != 200:
            print(f"page:{i}停止了下载")
            return
        idol_img_json = json.loads(response.text)
        image_list = re.findall(ex, idol_img_json['content'])  # 找到12个链接
        image_list_link = ['https://kpopping.com' + x for x in image_list]
        print(len(image_list_link), "单次下载长度", f"第{i}页")
        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.map(get_pic_link, image_list_link)


def get_pic_link(link):
    d_link = []
    r = requests.get(link, headers=headers).text
    ex = '<a href="/documents/(.*?)" data'
    p = re.findall(ex, r)
    for i in p:
        d_link.append("https://kpopping.com/documents/" + i)
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(download_one_pic, d_link)


if __name__ == "__main__":
    get_download_link()
