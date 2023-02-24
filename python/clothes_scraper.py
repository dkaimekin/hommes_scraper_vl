from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd

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
    max_pagination_number = (pagination_block.find_all(
        "button", class_="jss642")[-2].find("span", class_="jss641").text)
    return int(max_pagination_number)


def extractLinksFromPage(page: str) -> list[str]:
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

urls = {
    "women_clothes": "https://viled.kz/women/catalog/1320",
    "men_clothes": "https://viled.kz/men/catalog/1320"
}


def extractLinksFromCatalog(url: str, catalog_name: str) -> list[str]:
    extracted_links = []
    filename = catalog_name + ".html"
    cachePage(url, filename)
    cached_page = openCachedPage(filename)
    catalog_length = getCatalogPaginationLength(cached_page)
    for i in range(1, 3):  #catalog_length + 1):
        cachePage(url + "?page={0}".format(i), filename)
        print("Page {0} cached!".format(i))
        current_page = openCachedPage(filename)
        ###################################################
        # Testing extraction correctness
        # print(extractLinksFromPage(current_page))
        ###################################################
        extracted_links += extractLinksFromPage(current_page)
    return extracted_links


def extractDataFromItemPage(url: str) -> list[dict]:
    products_data = []
    filename = "clothes_item.html"
    cachePage(url, filename)
    cachedPage = openCachedPage(filename)
    for code in re.findall(r"}}],\"article\":\"(.*?)\"", cachedPage):
        product_data = {}
        product_data.update({"code": code})
        product_data.update({"size": re.search(
            r"_(.*?)_",
            code,
        ).group(1)})
        product_data.update({
            "brand":
            re.search(r"brand\":{\"name\":\"(.*?)\"",
                      cachedPage).group(1).upper()
        })
        product_data.update({
            "name":
            re.search(r"brand\":{.*\"nameRu\":\"(.*?)\"", cachedPage).group(1)
        })
        product_data.update({
            "price":
            re.search(r"\"id\":[0-9]+,\"price\":(.*?),", cachedPage).group(1)
        })
        product_data.update({
            "real_price":
            re.search(r"\"price\":[0-9]+,\"realPrice\":(.*?),",
                      cachedPage).group(1)
        })
        product_data.update({
            "composition_full":
            re.sub(
                r"([0-9]+(\.[0-9]+)?)", r" \1 ",
                re.search(r"Composition.*{\"value\":(.*?)\",",
                          cachedPage).group(1)).strip()
        })
        product_data.update({
            "description":
            re.search(r"descriptionRu\":\"(.*?)\"", cachedPage).group(1)
        })
        product_data.update({
            "material_clothes":
            re.search(r"Основной материал.*\"nameRu\":(.*?),.*9162",
                      cachedPage).group(1)
        })
        product_data.update({
            "images":
            "///".join(re.findall(r"original\":\"(.*?)\"", cachedPage))
        })
        print(product_data)
        products_data.append(product_data)
    return products_data


# extractDataFromItemPage("https://viled.kz/women/item/274253")


def scrapeDataFromSingleCatalog(url, catalog_name):
    links = extractLinksFromCatalog(url, catalog_name)
    products_data = []
    for link in links:
        products_data += extractDataFromItemPage("https://viled.kz" + link)

    dataframe = pd.DataFrame.from_dict(products_data)
    dataframe.to_csv("{0}.csv".format(catalog_name), sep=',', encoding='utf-8')


def scrapeDataFromMultipleCatalogs(url_dict):
    for key in url_dict:
        scrapeDataFromSingleCatalog(url_dict[key], key)
