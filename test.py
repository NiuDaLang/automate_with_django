from bs4 import BeautifulSoup
import requests

# Example 1
# url = "https://webscraper.io/test-sites/tables"
# response = requests.get(url)
# soup = BeautifulSoup(response.content, "html.parser")

# headings1 = soup.find_all("h1")
# headings2 = soup.find_all("h2")
# images = soup.find_all("img")

# table = soup.find_all("table")[1]
# rows = table.find_all("tr")[1:]

# last_names = []
# for row in rows:
#   last_names.append(row.find_all("td")[2].get_text())  

# Example 2
url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
custom_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
}
response = requests.get(url, headers=custom_headers)
soup = BeautifulSoup(response.content, "html.parser")

datatype_table = soup.find(class_="wikitable")
body = datatype_table.find("tbody")
rows = body.find_all("tr")[1:]

mutable_types = []
immutable_types = []

for row in rows:
    data = row.find_all("td")
    if data[1].get_text() == "mutable\n":
        mutable_types.append(data[0].get_text().strip())
    elif data[1].get_text() == "immutable\n":
        immutable_types.append(data[0].get_text().strip())

print(f"Mutable Types: {mutable_types}")
print(f"Immutable Types: {immutable_types}")