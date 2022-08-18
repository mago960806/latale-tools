import httpx
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor

url = "https://la.mangot5.com/game/la/notice/detail/"


def print_notice_title(notice_id: int) -> None:
    response = httpx.get(
        url,
        params={"contentNo": notice_id},
        verify=False,
        proxies={"http://": "http://127.0.0.1:7890", "https://": "http://127.0.0.1:7890"},
    )
    notice_id += 1
    selector = Selector(response.text)
    title = selector.xpath('//*[@id="main-l"]/table/tr/th/b/text()').get()
    if title:
        print(f"{response.request.url}: {title}")
    else:
        pass
        # print(f"{response.request.url}: skiped")


def main():
    notice_id = 50714
    with ThreadPoolExecutor(max_workers=10) as pool:
        tasks = pool.map(print_notice_title, [notice_id + i for i in range(500)])

    list(tasks)


main()
