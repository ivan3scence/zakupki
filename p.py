import requests
from bs4 import BeautifulSoup
from sys import getdefaultencoding


headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

url = f"https://e-legrand.ru/catalog/vyklyuchateli_i_pereklyuchateli/vyklyuchatel_dvukhklavishnyy_10a_slonovaya_kost_valena/"

req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")
print(soup.find(class_="page-title").text)