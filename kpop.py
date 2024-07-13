import concurrent.futures
import json
import re

import requests

'''
https://kpopping.com/kpics/240710-KARINA-Instagram-Update-with-GISELLE

下载链接 ；https://kpopping.com/kpics/download/240709-KARINA-Instagram-Update
'''
headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

'''
https://kpopping.com/kpics/240705-HYERI-Instagram-Update-with-KARINA

https://kpopping.com/documents/bd/1/800/240705-HYERI-Instagram-Update-with-KARINA-documents-3.jpeg?v=2ba21
'''


def download_one_pic(link: str):
    pic_content = requests.get(link, headers=headers)
    pic_name = link.split('.')[1].split('/')[-1]
    with open(f"result/{pic_name}.jpeg", "wb") as file:
        file.write(pic_content.content)


def get_download_link():
    ex = '<a href="(.*?)" class="cell" aria-label="album">'
    ret = []

    image_list_link = []
    page_count = 0
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
    ex = '<img src="/documents/(.*?)" alt='
    p = re.findall(ex, r)
    for i in p:
        d_link.append("https://kpopping.com/documents/" + i)
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(download_one_pic, d_link)


def downloader(link: str):
    '''
    <img src="/documents/bd/1/800/240705-HYERI-Instagram-Update-with-KARINA-documents-3.jpeg?v=2ba21" alt=

    :param link:
    :return:
    '''
    a = link.split('/')[-1]
    d = r'https://kpopping.com/kpics/' + a
    c = requests.get(d)
    # print(c.text)
    ex = '<img src="/documents/(.*?)" alt='
    p = re.findall(ex, c.text)
    print(p)
    print(len(p))
    for l in p:
        print("https://kpopping.com/documents/" + l)

        with open(f"result/{l.split('/')[3]}.jpg", "wb") as f:
            f.write(requests.get(url=("https://kpopping.com/documents/" + l)).content)


if __name__ == "__main__":
    # pass
    get_download_link()
    # downloader('/kpics/240705-HYERI-Instagram-Update-with-KARINA')
    # download_one_pic("https://kpopping.com/documents/bd/1/800/240705-HYERI-Instagram-Update-with-KARINA-documents-3.jpeg?v=2ba21")
