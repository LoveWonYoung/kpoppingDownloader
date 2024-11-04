import concurrent.futures
import itertools
import json
import os.path
import re
import time
import requests
import yaml

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 '
        'Safari/537.36'
}
# yaml解析
with open("config.yaml", "r", encoding="utf-8") as yaml_file:
    yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

idol = yaml_data["idol"]
total_page = yaml_data["total_page"]


def get_one_page_links(page):
    resp = requests.post(
        rf"https://kpopping.com/profiles/idol/{idol}/latest-pictures/{page}",
        headers=headers
    )
    if resp.status_code != 200:
        print("没有了")
        return
    idol_json = json.loads(resp.text)
    image_list = ['https://kpopping.com' + x for x in
                  re.findall('<a href="(.*?)" class="cell" aria-label="album">', idol_json['content'])]
    # print(image_list)
    return image_list


def make_download_dir(path):
    if not os.path.exists(fr"./result/{path}"):
        os.mkdir(fr"./result/{path}")
        print(f"文件夹 '{path}' 已创建。")
    else:
        print(f"文件夹 '{path}' 已存在，忽略创建。")


def downloader(link: str):
    # 得到文件夹名字
    dir_name = link.split('/')[-1]
    make_download_dir(dir_name)
    temp_text = requests.get(link, headers=headers).text
    r = ["https://kpopping.com/documents/" + x for x in re.findall('<a href="/documents/(.*?)" data', temp_text)]

    def download_one_picture(download_link: str):
        pic_content = requests.get(download_link, headers=headers)
        pic_name = link.split('.')[1].split('/')[-1]
        print(f"下载图片{pic_name}.jpeg")
        with open(fr"./result/{dir_name}/{pic_name}.jpeg", "wb") as file:
            file.write(pic_content.content)

    with concurrent.futures.ThreadPoolExecutor() as download_pool:
        download_pool.map(download_one_picture, r)


# def get_all_links():
#     with concurrent.futures.ThreadPoolExecutor() as pool:
#         result = list(pool.map(get_one_page_links, [x for x in range(1, total_page + 1)]))
#     # 第一次展开
#     links = list(itertools.chain(*result))
#     with concurrent.futures.ThreadPoolExecutor() as down_pool:
#         every_link = list(down_pool.map(downloader, links))
#     # 第二次展开
#     pic_links = list(itertools.chain(*every_link))
#     print(len(pic_links), pic_links)


# 一页一页的下载
def one_page_download():
    for p in range(1, total_page + 1):
        pages = get_one_page_links(p)
        if pages is not None:
            print(pages)
            print(f"第{p}页")
            with concurrent.futures.ThreadPoolExecutor() as req_pool:
                req_pool.map(downloader, pages)

        else:
            print(f"第{p}页下载结束")


if __name__ == '__main__':
    one_page_download()
