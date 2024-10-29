import concurrent.futures
import itertools
import json
import re
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


def get_every_link_pics_link(link: str):
    temp_text = requests.get(link, headers=headers).text
    return ["https://kpopping.com/documents/" + x for x in re.findall('<a href="/documents/(.*?)" data', temp_text)]


def get_all_links():
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = list(pool.map(get_one_page_links, [x for x in range(1, total_page + 1)]))
    # 第一次展开
    links = list(itertools.chain(*result))
    with concurrent.futures.ThreadPoolExecutor() as down_pool:
        every_link = list(down_pool.map(get_every_link_pics_link, links))
    # 第二次展开
    pic_links = list(itertools.chain(*every_link))
    print(len(pic_links), pic_links)


if __name__ == '__main__':
    get_all_links()
