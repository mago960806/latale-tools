import httpx
from parsel import Selector
import csv

cookies = {
    "_fbp": "fb.1.1639270991674.540732084",
    "_hjSessionUser_2400274": "eyJpZCI6IjdkYjlhMThlLTJlNmQtNWM3YS1iMDAxLTlkZTRmOWQ5MGRkMCIsImNyZWF0ZWQiOjE2Mzk2MzQ4Mzc4NTYsImV4aXN0aW5nIjp0cnVlfQ==",
    "_ga_CVD4E814M8": "GS1.1.1640337334.1.0.1640337465.0",
    "_ga": "GA1.1.346579012.1639270992",
    "JSESSIONID": "D58F7555EFF7559D91F8C12D276E6913",
    "_ga_KKH47LFCM4": "GS1.1.1644046910.44.0.1644046910.60",
    "_ga_F5C3895YN1": "GS1.1.1644046910.79.1.1644046918.52",
    "_ga_M57G7NJS00": "GS1.1.1644046910.80.1.1644046949.21",
}

headers = {
    "Proxy-Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "http://www.mangot5.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "http://www.mangot5.com/Index/blockUserBoard",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def get_rows(page: int):
    data = {"gname": "la", "charName": "", "offset": str(page)}
    response = httpx.post(
        "http://www.mangot5.com/Index/blockUserBoard", headers=headers, cookies=cookies, data=data, verify=False
    )
    selector = Selector(response.content.decode("utf-8"))
    trs = selector.xpath("//tbody/tr")
    rows = []
    for tr in trs:
        row = [td.get() for td in tr.xpath(".//td/text()")]
        rows.append(row)
    return rows


if __name__ == "__main__":
    with open("账号封禁记录.csv", "w", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["遊戲名稱", "伺服器", "角色名稱", "停權時間", "停權事由", "懲處方式"]
        writer = csv.writer(csv_file)
        writer.writerow(fieldnames)
        page = 0
        try:
            while True:
                rows = get_rows(page)
                writer.writerows(rows)
                print(f"第 {page} 页获取完毕")
                page += 1
        except Exception as e:
            print(e)
            pass
