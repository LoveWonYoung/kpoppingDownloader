import requests

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 '
        'Safari/537.36'
}


def my_test(page):
    resp = requests.post(
        rf"https://kpopping.com/profiles/idol/Wonyoung/latest-pictures/{page}",
        headers=headers
    )
    print(resp.status_code)


if __name__ == '__main__':
   my_test(60)