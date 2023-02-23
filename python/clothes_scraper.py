from bs4 import BeautifulSoup
import urllib.request

###################################################
# This is deprecated code, just for information purposes
# page = urllib.request.urlretrieve(
#     "https://viled.kz/women/catalog/1320", "catalog-page.html"
# )

# with open("./catalog-page.html", "r") as f:
#     webpage = f.read()


# soup = BeautifulSoup(webpage, "html.parser")
# print(len(soup.find_all("div", class_="jss25")))
# print(soup.find("h1").text)


# for tag in soup.find_all("div", class_="jss25"):
#     print(tag.find("a")["href"])
###################################################

###################################################
# Template URL for clothes is :
# https://viled.kz/women/catalog/1320?page=1
###################################################


def cachePage(url: str, page_name: str) -> None:
    # webpage = urllib.request.urlretrieve(url, "catalog-page-clothes.html")
    webpage = urllib.request.urlretrieve(url, page_name)
    print("Successfully cached page from {0}".format(url))


def openCachedPage(page_name: str) -> str:
    with open(page_name, "r") as f:
        cached_page = f.read()
    return cached_page


def getCatalogPaginationLength(page: str) -> int:
    soup = BeautifulSoup(page, "html.parser")
    pagination_block = soup.find("div", class_="jss643")
    max_pagination_number = (
        pagination_block.find_all("button", class_="jss642")[-2]
        .find("span", class_="jss641")
        .text
    )
    return int(max_pagination_number)


def extractLinks(page: str) -> list[str]:
    soup = BeautifulSoup(page, "html.parser")
    extracted_links = [
        tag.find("a")["href"] for tag in soup.find_all("div", class_="jss25")
    ]
    return extracted_links


###################################################
# Testing the methods
# cached_page = openCachedPage("catalog-page-clothes.html")
# print(getCatalogPaginationLength(cached_page))
###################################################

urls = {"women_clothes": "https://viled.kz/women/catalog/1320"}

for catalog_name in urls:
    filename = catalog_name + ".html"
    cachePage(urls[catalog_name], filename)
    cached_page = openCachedPage(filename)
    catalog_length = getCatalogPaginationLength(cached_page)
    for i in range(1, catalog_length + 1):
        cachePage(urls[catalog_name] + "?page={0}".format(i), filename)
        print("Page {0} cached!".format(i))
        current_page = openCachedPage(filename)
        print(extractLinks(current_page))
