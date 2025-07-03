# %%
import requests
from bs4 import BeautifulSoup

# %%
url = "https://www.melon.com/chart/index.htm"
header = {"User-Agent": "Mozilla/5.0"}

req = requests.get(url, headers=header)
soup = BeautifulSoup(req.text, "html.parser")
# 크롤링 가능 여부: 사이트/robots.txt
# %%
# 1 ~ 50 순위 앨범 곡 정보
tbody = soup.select_one("#frm > div > table > tbody")
lst50 = tbody.select("tr.lst50")
top50 = []
for td in lst50:
    rank = td.select_one("span.rank").get_text()
    title = td.select_one(
        "#lst50 > td:nth-child(6) > div > div > div.ellipsis.rank01 > span > a"
    ).get_text()
    singer = td.select_one(
        "#lst50 > td:nth-child(6) > div > div > div.ellipsis.rank02 > a"
    ).get_text()
    album = td.select_one("#lst50 > td:nth-child(7) > div > div > div > a").get_text()
    top50.append({"rank": rank, "title": title, "singer": singer, "album": album})
print(top50)
