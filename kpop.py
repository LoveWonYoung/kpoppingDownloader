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

# 分析解析数据
IDOLS = yaml_data["idol"]
TOTAL_PAGES = yaml_data["total_page"]
DOWNLOAD_PATH = yaml_data["path"]


class KpopDownload:
    def __init__(self, idol_name):
        self.idol_name = idol_name
        self.session = requests.Session()
        self.download()

    # 找到一页的所有请求链接
    def get_one_page_links(self, page):
        resp = self.session.post(
            rf"https://kpopping.com/profiles/idol/{self.idol_name}/latest-pictures/{page}",
            headers=headers
        )
        if resp.status_code != 200:
            print("这是最后一页了")
            return
        ex = '<a href="(.*?)" class="cell" aria-label="album">'
        idol_json = json.loads(resp.text)
        image_list = ['https://kpopping.com' + x for x in re.findall(ex, idol_json['content'])]
        return image_list

    def make_download_dir(self, path):
        # 拼接下载路径文件夹
        down_path = os.path.join(DOWNLOAD_PATH, self.idol_name, path)
        os.makedirs(down_path, exist_ok=True)

    def _downloader(self, link: str):
        # 得到文件夹名字
        dir_name = link.split('/')[-1]
        ex = '<a href="/documents/(.*?)" data'
        self.make_download_dir(dir_name)
        temp_text = self.session.get(link, headers=headers).text
        r = ["https://kpopping.com/documents/" + x for x in re.findall(ex, temp_text)]

        def download_one_picture(download_link: str):
            try:

                pic_content = self.session.get(download_link, headers=headers)
                pic_name = download_link.split('.')[1].split('/')[-1]
                full_pic_name = os.path.join(DOWNLOAD_PATH, self.idol_name, dir_name, pic_name)
                # 如果要下载的文件已存在就跳过下载
                if os.path.exists(full_pic_name + ".jpeg"):
                    print(f"已存在{full_pic_name}，跳过下载")
                    return
                print(f"下载图片{pic_name}.jpeg")
                with open(full_pic_name + ".jpeg", "wb") as file:
                    file.write(pic_content.content)

            except Exception as e:
                print(f"文件下载错误 {e}")

        with concurrent.futures.ThreadPoolExecutor() as download_pool:
            download_pool.map(download_one_picture, r)

    def download(self):
        # 一页一页的下载
        for p in range(1, TOTAL_PAGES + 1):
            pages = self.get_one_page_links(p)
            if pages is not None:
                print(f"第{p}页开始下载")
                with concurrent.futures.ThreadPoolExecutor() as req_pool:
                    req_pool.map(self._downloader, pages)
                print(f"第{p}页下载完成")
            else:
                print(f"第{p}页下载结束")


if __name__ == '__main__':
    for idol in IDOLS:
        print(f"下载{TOTAL_PAGES}页{idol}的图片")
        KpopDownload(idol)
