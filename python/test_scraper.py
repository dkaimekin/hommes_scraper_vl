from requests_html import HTMLSession
from bs4 import BeautifulSoup
import urllib.request

link = "https://viled.kz/women/catalog/1320"

# session = HTMLSession()

# r = session.get(link)

# r.html.render(sleep=5, keep_page=True, scrolldown=5)

# # Trying to use BeautifulSoup instead of html.find:
# soupInstance = BeautifulSoup(r.text, "html.parser")
# # print(
# #     soupInstance.find(
# #         "h1",
# #         class_="MuiBox-root jss763 jss25",
# #     ).text
# # )

# print(len(soupInstance.find_all("div", class_="MuiBox-root jss763 jss25")))

# print(r.text)

# print(len(soupInstance.find_all("div", class_="MuiBox-root jss763 jss25")))

page = urllib.request.urlretrieve("https://viled.kz/women/catalog/1320",
                                  "catalog-page.html")

with open("./catalog-page.html", "r") as f:
    webpage = f.read()

soup = BeautifulSoup(webpage, "html.parser")
print(len(soup.find_all("div", class_="jss25")))
print(soup.find("h1").text)

for tag in soup.find_all("div", class_="jss25"):
    print(tag.find("a")["href"])
