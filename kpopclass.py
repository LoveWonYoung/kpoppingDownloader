import concurrent.futures
import re
import json
import requests
import yaml
import os

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 '
        'Safari/537.36'
}
# yaml解析
with open("config.yaml", "r", encoding="utf-8") as yaml_file:
    yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

IDOLS = yaml_data["idol"]
TOTAL_PAGES = yaml_data["total_page"]
DOWNLOAD_PATH = yaml_data["path"]


class KpoppingDownloader:
    def __init__(self, idol_name):
        self.idol_name = idol_name
        self.one_page_download()
    # 找到一页的所有请求链接
    def get_one_page_links(self, page):
        resp = requests.post(
            rf"https://kpopping.com/profiles/idol/{self.idol_name}/latest-pictures/{page}",
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

    def make_download_dir(self, path):
        if not os.path.exists(DOWNLOAD_PATH + os.sep + self.idol_name):
            os.mkdir(DOWNLOAD_PATH + os.sep + self.idol_name)
        else:
            pass
        if not os.path.exists(DOWNLOAD_PATH + os.sep + self.idol_name + os.sep + path):
            os.mkdir(DOWNLOAD_PATH + os.sep + self.idol_name + os.sep + path)
        else:
            pass

    def downloader(self, link: str):
        # 得到文件夹名字
        dir_name = link.split('/')[-1]
        self.make_download_dir(dir_name)
        temp_text = requests.get(link, headers=headers).text
        r = ["https://kpopping.com/documents/" + x for x in re.findall('<a href="/documents/(.*?)" data', temp_text)]

        def download_one_picture(download_link: str):
            pic_content = requests.get(download_link, headers=headers)
            pic_name = download_link.split('.')[1].split('/')[-1]
            print(f"下载图片{pic_name}.jpeg")
            with open(DOWNLOAD_PATH + os.sep + self.idol_name + os.sep + dir_name + os.sep + pic_name + ".jpeg",
                      "wb") as file:
                file.write(pic_content.content)

        with concurrent.futures.ThreadPoolExecutor() as download_pool:
            download_pool.map(download_one_picture, r)

    def one_page_download(self):
        for p in range(1, TOTAL_PAGES + 1):
            pages = self.get_one_page_links(p)
            if pages is not None:
                print(f"第{p}页")
                with concurrent.futures.ThreadPoolExecutor() as req_pool:
                    req_pool.map(self.downloader, pages)
                print("下载完成")
            else:
                print(f"第{p}页下载结束")


if __name__ == '__main__':
    for idol in IDOLS:
        print(f"下载{TOTAL_PAGES}页{idol}的图片")
        d = KpoppingDownloader(idol)
