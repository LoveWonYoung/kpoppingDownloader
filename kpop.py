import concurrent.futures
import json
import os.path
import re

import requests

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}



def download_one_pic(link: str):
    pic_content = requests.get(link, headers=headers)
    pic_name = link.split('.')[1].split('/')[-1]
    with open(f"/Users/wonyoung/Desktop/karina/{pic_name}.jpeg", "wb") as file:
        file.write(pic_content.content)


def get_download_link():
    ex = '<a href="(.*?)" class="cell" aria-label="album">'
    image_list_link = []
    for i in range(60):
        response = requests.post(r"https://kpopping.com/profiles/idol/Karina2/latest-pictures/{}".format(i))
        if response.status_code != 200:
            return
        idol_img_json = json.loads(response.text)
        image_list = re.findall(ex, idol_img_json['content'])  # 找到12个链接
        print(image_list)
        for r_link in image_list:
            image_list_link.append('https://kpopping.com' + r_link)

        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.map(get_pic_link, image_list_link)


def get_pic_link(link):
    d_link = []
    r = requests.get(link, headers=headers).text
    # ex = '<img src="/documents/(.*?)" alt='
    ex = '<a href="/documents/(.*?)" data'
    '''
    <a href="/documents/2c/5/2730/240705-IVE-Yujin-Wonyoung-at-Hong-Kong-Fansign-Event-documents-1.jpeg?v=aca46" data-fancybox="gallery" data-hash="false" data-thumbs="false" style="--ratio:150.01500150015%;">
<img src="/documents/2c/5/800/240705-IVE-Yujin-Wonyoung-at-Hong-Kong-Fansign-Event-documents-1.jpeg?v=9270a" alt="240705 IVE Yujin, Wonyoung at Hong Kong Fansign Event documents 1">
</a>
    '''
    p = re.findall(ex, r)
    for i in p:
        d_link.append("https://kpopping.com/documents/" + i)
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(download_one_pic, d_link)


if __name__ == "__main__":
    get_download_link()
