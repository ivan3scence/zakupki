from multiprocessing import Pool
from dateutil.rrule import rrule, DAILY
from bs4 import BeautifulSoup as bs
from datetime import date
import requests
import re
import csv

from requests.api import post

a = date(2021, 11, 8)        # Начало периода
b = date(2021, 11, 9)       # конец периода
id_region = '5277335'       # id региона                       
thr = 5                     # кол-во потоков
record_file = 'boba.csv'  # файл с результатами
 
pages = 4

def urrll(i):
    url = f'https://zakupki.gov.ru/epz/contract/search/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&savedSearchSettingsIdHidden=&fz44=on&contractStageList_0=on&contractStageList=0&contractInputNameDefenseOrderNumber=&contractInputNameContractNumber=&contractPriceFrom=500000&rightPriceRurFrom=&contractPriceTo=&rightPriceRurTo=&priceToUnitGWS=&contractCurrencyID=-1&nonBudgetCodesList=&budgetLevelsIdHidden=&budgetLevelsIdNameHidden=%7B%7D&budgetName=&customerPlace=5277335%2C5277327&customerPlaceCodes=77000000000%2C50000000000&contractDateFrom=08.11.2021&contractDateTo=10.11.2021&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&placingWayList=&selectedLaws=&sortBy=UPDATE_DATE&pageNumber={i}&sortDirection=false&recordsPerPage=_500&showLotsInfoHidden=false'
    return url

def request_url(url):
    """Получаем страницу"""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/71.0.3578.98 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers).text
        soup = bs(r, 'html.parser')
        return soup
    except Exception as e:
        print(e)


def clear(text):
    """Очистка текста"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' ₽\n', '', text)
    text = text.lstrip()
    text = text.rstrip()
    return text


def pr_csv(listik):
    with open(record_file, "a", encoding="utf-8") as file_3:
        writer = csv.writer(file_3)
        for data in listik:
            writer.writerow(data)

def parser_start(soup):
    """Парсер данных"""
    listik = []
    block = soup.find_all(class_="row no-gutters registry-entry__form mr-0")   #every zakupka
    print(len(block))
    try:
        for item in block:
        # item = block[0]
            text_nm = item.find('div', {'class': 'registry-entry__header-mid__number'}).text
            text_nm = clear(text_nm)  # Код аукциона                                                  
            text_ur = "https://zakupki.gov.ru/" + item.find('div', {'class': 'registry-entry__header-mid__number'}).findAll('a')[0].get(
                'href')  # url kontr                                                                  
            # print(text_ur)
            text_zk = item.find('div', {'class': 'registry-entry__body-href'}).text        
            text_zk = clear(text_zk)  # Заказчик
            # print(text_zk)
            nsoup = request_url(text_ur)
            # print(nsoup)
            text_pr = nsoup.find(class_='price').find(class_='cardMainInfo__content cost').text.strip()         #price
            blocks = nsoup.find_all(class_="blockInfo__section section")
            text_sn = ""
            text_dn = ""
            text_dk = ""
            try:
                for bss in blocks:
                    if bss.find(class_="section__title").text == "Сокращенное наименование заказчика":
                        text_sn = bss.find(class_="section__info").text                           #краткое наименование заказчика
                        
                    if bss.find(class_="section__title").text == "ИНН":
                        text_inn = bss.find(class_="section__info").text.strip()                      #инн заказчика
                        
                    if bss.find(class_="section__title").text == "Дата начала исполнения контракта":
                        text_dn = clear(bss.find(class_="section__info").text)                  #дата начала исп заказа
                    
                    if bss.find(class_="section__title").text == "Дата окончания исполнения контракта":
                        text_dk = clear(bss.find(class_="section__info").text)                  #дата конца исп заказа


            except Exception as ex:
                1 + 1
                # print(ex)
                # print(text_nm, text_zk, text_sn, text_inn, text_dn, text_dk)
            # print(text_sn)
            
            text_np = text_np_ooo = ""
            np = nsoup.find(class_='tableBlock__col tableBlock__col_first text-break').text.split('\n')
            try:
                post_inn = nsoup.find(class_='tableBlock__col tableBlock__col_first text-break').find_all(class_="section")#[1].text.strip().split('\n')[1]
                # print(np)
                for h in post_inn:
                    if h.text.strip().split('\n')[0] == "ИНН:":
                        text_post_inn = h.text.strip().split('\n')[1]
            except Exception as e:
                print(e)
            for i in np:
                if i != "":
                    text_np = i.strip()     #название поставщика
                    try:
                        text_np_ooo = text_np[1+ text_np.find("("):text_np.find(")")].strip()
                        ip = text_np_ooo.find("Индивидуальный")
                        if (ip != -1):
                            text_np_ooo = "ИП " + text_np_ooo[:ip]
                        else:# text_np_ooo.upper().find("ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ") or text_np_ooo.upper().find("АКЦИОНЕРНОЕ ОБЩЕСТВО") or text_np_ooo.upper().find("ЗАКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО") or text_np_ooo.upper().find("ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО") or text_np_ooo.upper().find("АВТОНОМНАЯ НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ"):
                            iooo = text_np_ooo.upper().find("ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ")
                            if iooo != -1:
                                text_np_ooo = text_np_ooo[:iooo] + "ООО " + text_np_ooo[iooo + 41:]
                            ipao = text_np_ooo.upper().find("ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО")
                            if ipao != -1:
                                text_np_ooo = text_np_ooo[:ipao] + "ПАО " + text_np_ooo[ipao + 41:]
                            izao = text_np_ooo.upper().find("ЗАКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО")
                            if izao != -1:
                                text_np_ooo = text_np_ooo[:izao] + "ЗАО " + text_np_ooo[izao + 31:]
                            ia = text_np_ooo.upper().find("АКЦИОНЕРНОЕ ОБЩЕСТВО")
                            if ia != -1:
                                text_np_ooo = text_np_ooo[:ia] + "АО " + text_np_ooo[ia + 21:]
                            iz = text_np_ooo.upper().find("ЗАКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО")
                            if iz != -1:
                                text_np_ooo = text_np_ooo[:iz] + "ЗАО " + text_np_ooo[iz + 30:]
                            iano = text_np_ooo.upper().find("АВТОНОМНАЯ НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ")
                            if iano != -1:
                                text_np_ooo = text_np_ooo[:iano] + "АНО " + text_np_ooo[iano + 38:]
                        


                    except Exception as e:
                        print("ooo rip", e)
                    break
            print(text_np_ooo)
            col = nsoup.find_all(class_="col")#[-1]
            for n in col:
                pp = n.find(class_="blockInfo__title")
                if pp:
                    if pp.text.strip() == "Информация о поставщиках":
                        col = n
                        break
            if isinstance(col, list):
                col = 0
            # print(col)
            text_tp = text_mp = text_ap = ""
            if col:
                postav = col.find_all(class_="tableBlock__col")
                length = len(postav)
                if (length == 15):
                    length = 10
                i_adres_mest = i_tel_po = 0
                for i in range(length):
                    # print(postav[i].text.replace('\n', '').strip())
                    if postav[i].text.replace('\n', '').strip() == "Адрес места нахождения":
                        i_adres_mest = i
                    elif postav[i].text.replace('\n', '').strip() == "Телефон, электронная почта":
                        i_tel_po = i
                    
                # print(i_adres_mest, i_tel_po)
                if i_adres_mest:
                    text_ap = postav[length // 2 + i_adres_mest].text.replace('\n', '').strip()
                else:
                    text_ap = ""
                if i_tel_po:
                    tp = postav[length // 2 + i_tel_po].text.replace('\n', '').strip()
                    ii = 0
                    for ii, c in enumerate(tp):
                        if (c.isalpha() or c.isnumeric()) and ii > 21:
                            break
                    if ii == 0:
                        text_tp = tp.strip()
                        text_mp = ""
                    else:
                        text_tp = tp[:ii].strip()   #телефон
                        text_mp = tp[ii:].strip()    #мыло   
                else:
                    text_tp = text_mp = ""

            data_item = (text_nm, text_ur, text_pr, text_zk, text_sn, text_inn, text_dn, text_dk, text_np, text_np_ooo.strip(), text_post_inn, text_ap, text_tp, text_mp)
            listik.append(data_item)
    except Exception as e:
        print(e)
    pr_csv(listik)

with open(record_file, "w", encoding="utf-8") as file_3:
        writer = csv.writer(file_3)
        writer.writerow(
            (
                "Реестровый номер контракта",
                "Ссылка на контракт",
                "Цена контракта",
                "Полное наименование заказчика",
                "Сокращенное наименование заказчика",
                "ИНН",
                "Дата начала исполнения контракта",
                "Дата окончания исполнения контракта",
                "Наименование поставщика",
                "Сокращенное наименование поставщика",
                "ИНН поставщика",
                "Адрес поставщика",
                "Телефон поставщика",
                "Почта Поставщика"
            )
        )

print ('Начинаю сбор данных, подождите...')
ist = 1
while (pages >= ist):
    arr_url = urrll(ist)
    ist = ist + 1
    date_array = request_url(arr_url)   #doing soup
    parser_start(date_array)