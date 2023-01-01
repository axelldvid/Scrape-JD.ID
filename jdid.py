import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.edge.options import Options



def parser(link='https://www.jd.id/') :
    options = Options()
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    driver = webdriver.Edge(options=options)
    driver.get(link)
    driver.implicitly_wait(10)
    for i in range(43):
        driver.execute_script("window.scrollBy(0, 250)")
        time.sleep(0.2)
    soup = bs(driver.page_source,"lxml")
    driver.close()
    return soup

def search_items():
    datascrape={}
    cari = input('\nMasukkan Barang Yang Ingin Dicari : ').title()
    soup = parser(f'https://www.jd.id/search?keyword={cari}')
    if cari == 'Laptop':
        laptop=['Asus','Acer','Apple','Lenovo','Hp']
        listlaptop=[]
        print('Pilih Brand:')
        i=0
        for item in soup.findAll('a', class_ = 'item'):
            brand = item.find('p', class_ = 'brand-name').text.title()
            link = item['href']
            if brand in laptop:
                i += 1
                print(f'{i}. {brand}')
                listlaptop.append([brand,link])
        pilih = input("Pilihan Anda: ")
        i=0
        for [x,y] in listlaptop:
            if x == pilih:
                soup = parser(y)
                for barang in soup.findAll('a', class_ = 'sku-info'):
                    i += 1
                    nama = barang.find('div', class_ = 'p-name')['title']
                    toko = barang.find('div', class_ = 'p-store')['title']
                    harga = int(barang.find('div', class_ = 'p-price').span.text.replace(' ', '').replace(',', ''))
                    datascrape.update({i: {'Nama': nama, 'Toko': toko, 'Harga': harga}})
                break
        cari=cari+pilih

    elif cari == 'Handphone' or cari == 'Smartphone':
        handphone=['Asus','Apple','Google','Oppo','Vivo','Xiaomi','Samsung','Infinix']
        listhp=[]
        print('Pilih Brand:')
        i=0
        for item in soup.findAll('a', class_ = 'item'):
            brand = item.find('p', class_ = 'brand-name').text.title()
            link = item['href']
            if brand in handphone:
                i += 1
                print(f'{i}. {brand}')
                listhp.append([brand,link])
        pilih = input("Pilih Brand : ")
        i=0
        for [x,y] in listhp:
            if x == pilih:
                soup = parser(y)
                for barang in soup.findAll('a', class_ = 'sku-info'):
                    i += 1
                    nama = barang.find('div', class_ = 'p-name')['title']
                    toko = barang.find('div', class_ = 'p-store')['title']
                    harga = int(barang.find('div', class_ = 'p-price').span.text.replace(' ', '').replace(',', ''))
                    datascrape.update({i: {'Nama': nama, 'Toko': toko, 'Harga': harga}})
                break
        cari=cari+pilih
        
    else :
        i = 0
        for barang in soup.findAll('a', class_ = 'sku-info'):
            i += 1
            nama = barang.find('div', class_ = 'p-name')['title']
            toko = barang.find('div', class_ = 'p-store')['title']
            harga = int(barang.find('div', class_ = 'p-price').span.text.replace(' ', '').replace(',', ''))
            datascrape.update({i: {'Nama': nama, 'Toko': toko, 'Harga': harga}})

    df = pd.DataFrame.from_dict(datascrape, orient='index')
    file = df.to_csv("C:\\Users\\axeld\\Documents\\22'23\\PBO\\Coding\\Python Course\\PBO\\Minggu 12\\scrape_"+cari+".csv", index=False)
    return file

def superdeal_items():
    soup = parser()
    superdeal = soup.find('div', class_ = 'product-list')
    i = 0
    for item in superdeal.findAll('div', class_ = 'switch-product-item') :
        nama=item.find('a', class_ = 'title').text.title()
        harga=int(item.find('div', class_ = 'jd-price').text.strip('Rp').replace(' ','').replace(',',''))
        diskon=int(item.find('span', class_ = 'disCount superDeal').text.strip('-%').replace(' ',''))
        promo=int(item.find('div', class_ = 'promo-price').text.strip('Rp').replace(' ','').replace(',','')[:-4])
        link='https:'+item.find('a', class_ = 'link')['href']
        i += 1
        #datascrape.update({i: {'Nama': nama, 'Harga': harga, 'Diskon': diskon, 'Promo': promo, 'Link' : link}})
    

print('Pilih Mode:')
print('1. Cari Items')
print('2. Superdeal Items')
print('3. Exit')
mode = input('Pilihan Anda: ').title()

if mode in ['1', 'Search', 'Items', 'Search Items'] :
    filescrape = search_items()
elif mode in ['2', 'Superdeal', 'Superdeal Items']:
    filesuperdeal = superdeal_items()
elif mode == 3 :
    exit()
