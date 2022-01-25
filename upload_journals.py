from dataclasses import asdict, dataclass

import httpx
from jinja2 import Template
from parsel import Selector


@dataclass
class Journal:
    title: str
    image_url: str
    page_url: str

    def dict(self):
        return asdict(self)


def get_journals():
    url = "https://la.mangot5.com/game/la/journal"
    headers = {
        "authority": "la.mangot5.com",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
        "referer": "https://la.mangot5.com/game/la/event?page=&type=now&searchText=",
    }

    page = 1
    journals = []
    while True:
        params = {"page": page}
        response = httpx.get(url, headers=headers, params=params)
        select = Selector(response.text)
        for element in select.xpath("//div[@class='revision']/ul/li"):
            title = element.xpath("./div/nobr/text()").get().strip()
            image_url = "https:" + element.xpath("./a/img/@src").get().replace("//Images", "/Images")
            page_url = element.xpath("./a/@href").get()
            journal = Journal(title=title, image_url=image_url, page_url=page_url)
            journals.append(journal)
        if "Next" not in response.text:
            break
        else:
            page += 1
    return journals


if __name__ == "__main__":
    journals = get_journals()
    with open("templates/journals.jinja2") as f:
        template = Template(f.read(), trim_blocks=True)
    print(template.render(journals=journals))
