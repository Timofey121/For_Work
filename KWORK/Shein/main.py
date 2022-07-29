# -*- coding: utf8 -*-
import csv
import random
import time
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

Additional_Percentage_To_The_Price = 0.00

URLS = {
    'https://www.shein.co.uk/Women-Clothing-c-2030.html?ici=CCCSN=WomenHomePage_ON=Banner_OI=1_CN=shopbycat_TI=50001_aod=0_PS=HZ-5-11_ABT=0&scici=WomenHomePage~~ON_Banner,CN_shopbycat,HZ_viewall,HI_hotZonenf8o8syzglm~~5_11~~real_2030~~~~&srctype=homepage&userpath=-WomenHomePage-Women-Clothing&src_module=WomenHomePage&src_identifier=on%3DBanner%60cn%3Dshopbycat%60hz%3Dviewall%60ps%3D5_11%60jc%3Dreal_2030&src_tab_page_id=page_home1656931881930': "Women Clothing",
    'https://www.shein.co.uk/Women-Dresses-c-1727.html?ici=uk_tab01navbar05&scici=navbar_WomenHomePage~~tab01navbar05~~5~~real_1727~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657140061077&src_identifier=fc%3DWomen%60sc%3DDRESSES%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar05%60jc%3Dreal_1727&srctype=category&userpath=category-DRESSES': 'Women Dresses',
    'https://www.shein.co.uk/Women-Beachwear-c-2039.html?ici=uk_tab01navbar06&scici=navbar_WomenHomePage~~tab01navbar06~~6~~real_2039~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657140080608&src_identifier=fc%3DWomen%60sc%3DBEACHWEAR%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar06%60jc%3Dreal_2039&srctype=category&userpath=category-BEACHWEAR': 'Women Beachwear',
    'https://www.shein.co.uk/category/Women-Lingerie-Loungwear-sc-00856812.html?ici=uk_tab01navbar08&scici=navbar_WomenHomePage~~tab01navbar08~~8~~itemPicking_00856812~~~~0': 'Women Lingerie Loungwear',
    'https://www.shein.co.uk/Sports-c-3195.html?ici=uk_tab01navbar09&scici=navbar_WomenHomePage~~tab01navbar09~~9~~real_3195~~~~0&src_module=topcat&src_tab_page_id=page_select_class1657140152115&src_identifier=fc%3DWomen%60sc%3DACTIVEWEAR%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar09%60jc%3Dreal_3195&srctype=category&userpath=category-ACTIVEWEAR': 'Sports',
    'https://www.shein.co.uk/category/Shoes-Bags-Accs-sc-00828516.html?ici=uk_tab01navbar10&scici=navbar_WomenHomePage~~tab01navbar10~~10~~webLink~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657140190896&src_identifier=fc%3DWomen%60sc%3DSHOES%20%26%20ACCESSORIES%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar10%60jc%3Durl_https%253A%252F%252Fwww.shein.co.uk%252Fcategory%252FShoes-Bags-Accs-sc-00828516.html&srctype=category&userpath=category-SHOES-ACCESSORIES': 'Shoes Bags Accs',
    'https://www.shein.co.uk/Women-Plus-Clothing-c-1888.html?ici=uk_tab02navbar04&scici=navbar_PlussizeHomePage~~tab02navbar04~~4~~real_1888~~~~0&src_module=topcat&src_tab_page_id=page_home1657140259454&src_identifier=fc%3DPlussize%60sc%3DCLOTHING%60tc%3D0%60oc%3D0%60ps%3Dtab02navbar04%60jc%3Dreal_1888&srctype=category&userpath=category-CLOTHING': 'Women Plus Clothing',
    'https://www.shein.co.uk/Plus-Size-Dresses-c-1889.html?ici=uk_tab02navbar05&scici=navbar_PlussizeHomePage~~tab02navbar05~~5~~real_1889~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657140266923&src_identifier=fc%3DPlussize%60sc%3DDRESSES%60tc%3D0%60oc%3D0%60ps%3Dtab02navbar05%60jc%3Dreal_1889&srctype=category&userpath=category-DRESSES': 'Plus Size Dresses',
    'https://www.shein.co.uk/Plus-Size-Beachwear-c-3613.html?ici=uk_tab02navbar06&scici=navbar_PlussizeHomePage~~tab02navbar06~~6~~real_3613~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657140296841&src_identifier=fc%3DPlussize%60sc%3DBEACHWEAR%60tc%3D0%60oc%3D0%60ps%3Dtab02navbar06%60jc%3Dreal_3613&srctype=category&userpath=category-BEACHWEAR': 'Plus Size Beachwear',
    'https://www.shein.co.uk/Plus-Size-Tops-c-2225.html?ici=uk_tab02navbar07&scici=navbar_PlussizeHomePage~~tab02navbar07~~7~~real_2225~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657140424046&src_identifier=fc%3DPlussize%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab02navbar07%60jc%3Dreal_2225&srctype=category&userpath=category-TOPS': 'Plus Size Tops',
    'https://www.shein.co.uk/Plus-Size-Bottoms-c-2226.html?ici=uk_tab02navbar08&scici=navbar_PlussizeHomePage~~tab02navbar08~~8~~real_2226~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657140450013&src_identifier=fc%3DPlussize%60sc%3DBOTTOMS%60tc%3D0%60oc%3D0%60ps%3Dtab02navbar08%60jc%3Dreal_2226&srctype=category&userpath=category-BOTTOMS': 'Plus Size Bottoms',
    'https://www.shein.co.uk/category/Plus-Size-Lingerie-Lounge-sc-00806321.html?ici=uk_tab02navbar09&scici=navbar_PlussizeHomePage~~tab02navbar09~~9~~itemPicking_00806321~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657140475991&src_identifier=fc%3DPlussize%60sc%3DLINGERIE%20%26%20LOUNGE%60tc%3D0%60oc%3D0%60ps%3Dtab02navbar09%60jc%3DitemPicking_00806321&srctype=category&userpath=category-LINGERIE-LOUNGE': 'Plus Size Lingerie & Loungewear',
    'https://www.shein.co.uk/Women-Plus-Activewear-c-2491.html?ici=uk_tab02navbar10&scici=navbar_PlussizeHomePage~~tab02navbar10~~10~~real_2491~~~~0&src_module=topcat&src_tab_page_id=page_select_class1657140526541&src_identifier=fc%3DPlussize%60sc%3DACTIVEWEAR%60tc%3D0%60oc%3D0%60ps%3Dtab02navbar10%60jc%3Dreal_2491&srctype=category&userpath=category-ACTIVEWEAR': 'Women Plus Activewear',
    'https://www.shein.co.uk/category/Kids-Accs-Shoes-sc-00825263.html?ici=uk_tab03navbar11&scici=navbar_KidsHomePage~~tab03navbar11~~11~~itemPicking_00825263~~~~0&src_module=topcat&src_tab_page_id=page_home1657140565526&src_identifier=fc%3DKids%60sc%3DACCESSORIES%20%26%20SHOES%60tc%3D0%60oc%3D0%60ps%3Dtab03navbar11%60jc%3DitemPicking_00825263&srctype=category&userpath=category-ACCESSORIES-SHOES': 'Kids Accs',
    "https://www.shein.co.uk/Men-Clothing-c-2026.html?ici=uk_tab04navbar04menu01&scici=navbar_MenHomePage~~tab04navbar04menu01~~4_1~~real_2026~~~~0&src_module=topcat&src_tab_page_id=page_real_class1656937049403&src_identifier=fc%3DMen%60sc%3DCLOTHING%60tc%3DVIEW%20ALL%60oc%3D0%60ps%3Dtab04navbar04menu01%60jc%3Dreal_2026&srctype=category&userpath=category-CLOTHING-VIEW-ALL&child_cat_id=1973": "Men Clothing",
    'https://www.shein.co.uk/Men-Tops-c-1970.html?ici=uk_tab04navbar05&scici=navbar_MenHomePage~~tab04navbar05~~5~~real_1970~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657139884974&src_identifier=fc%3DMen%60sc%3DTOPS%60tc%3D0%60oc%3D0%60ps%3Dtab04navbar05%60jc%3Dreal_1970&srctype=category&userpath=category-TOPS': 'Men Tops',
    'https://www.shein.co.uk/Men-Bottoms-c-2045.html?ici=uk_tab04navbar06&scici=navbar_MenHomePage~~tab04navbar06~~6~~real_2045~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657139895963&src_identifier=fc%3DMen%60sc%3DBOTTOMS%60tc%3D0%60oc%3D0%60ps%3Dtab04navbar06%60jc%3Dreal_2045&srctype=category&userpath=category-BOTTOMS': 'Men Bottoms',
    'https://www.shein.co.uk/Men-Swimwear-c-3792.html?ici=uk_tab04navbar07&scici=navbar_MenHomePage~~tab04navbar07~~7~~real_3792~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657139923339&src_identifier=fc%3DMen%60sc%3DSWIMWEAR%60tc%3D0%60oc%3D0%60ps%3Dtab04navbar07%60jc%3Dreal_3792&srctype=category&userpath=category-SWIMWEAR': 'Men Swimwear',
    'https://www.shein.co.uk/category/Men-Shoes-Accessories-sc-00811755.html?ici=uk_tab04navbar08&scici=navbar_MenHomePage~~tab04navbar08~~8~~itemPicking_00811755~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657139946074&src_identifier=fc%3DMen%60sc%3DSHOES%20%26%20ACCESSORIES%60tc%3D0%60oc%3D0%60ps%3Dtab04navbar08%60jc%3DitemPicking_00811755&srctype=category&userpath=category-SHOES-ACCESSORIES': "Men's Shoes & Accessories",
    'https://www.shein.co.uk/category/Baby-sc-00861365.html?ici=uk_tab03navbar05menu01&scici=navbar_KidsHomePage~~tab03navbar05menu01~~5_1~~itemPicking_00861365~~~~0&src_module=topcat&src_tab_page_id=page_home1656931976031&src_identifier=fc%3DKids%60sc%3DBABY%60tc%3DVIEW%20ALL%60oc%3D0%60ps%3Dtab03navbar05menu01%60jc%3DitemPicking_00861365&srctype=category&userpath=category-BABY-VIEW-ALL': 'Baby(0-3yrs)',
    'https://www.shein.co.uk/Toddler-Boys-Clothing-c-2059.html?ici=uk_tab03navbar06menu01&scici=navbar_KidsHomePage~~tab03navbar06menu01~~6_1~~real_2059~~~~0&src_module=topcat&src_tab_page_id=page_home1656931976031&src_identifier=fc%3DKids%60sc%3DYOUNGER%20BOYS%60tc%3DVIEW%20ALL%60oc%3D0%60ps%3Dtab03navbar06menu01%60jc%3Dreal_2059&srctype=category&userpath=category-YOUNGER-BOYS-VIEW-ALL': 'Younger Boys(1-7yrs)',
    'https://www.shein.co.uk/Toddler-Girls-Clothing-c-2058.html?ici=uk_tab03navbar07menu01&scici=navbar_KidsHomePage~~tab03navbar07menu01~~7_1~~real_2058~~~~0&src_module=topcat&src_tab_page_id=page_home1656931976031&src_identifier=fc%3DKids%60sc%3DYOUNGER%20GIRLS%60tc%3DVIEW%20ALL%60oc%3D0%60ps%3Dtab03navbar07menu01%60jc%3Dreal_2058&srctype=category&userpath=category-YOUNGER-GIRLS-VIEW-ALL': 'Younger Girls(1-7yrs)',
    'https://www.shein.co.uk/Boys-Clothing-c-1990.html?ici=uk_tab03navbar08menu01&scici=navbar_KidsHomePage~~tab03navbar08menu01~~8_1~~real_1990~~~~0&src_module=topcat&src_tab_page_id=page_home1656931976031&src_identifier=fc%3DKids%60sc%3DOLDER%20BOYS%60tc%3DVIEW%20ALL%60oc%3D0%60ps%3Dtab03navbar08menu01%60jc%3Dreal_1990&srctype=category&userpath=category-OLDER-BOYS-VIEW-ALL': 'Older Boys(7-14yrs)',
    'https://www.shein.co.uk/Girls-Clothing-c-1991.html?ici=uk_tab03navbar09menu01&scici=navbar_KidsHomePage~~tab03navbar09menu01~~9_1~~real_1991~~~~0&src_module=topcat&src_tab_page_id=page_home1656931976031&src_identifier=fc%3DKids%60sc%3DOLDER%20GIRLS%60tc%3DVIEW%20ALL%60oc%3D0%60ps%3Dtab03navbar09menu01%60jc%3Dreal_1991&srctype=category&userpath=category-OLDER-GIRLS-VIEW-ALL': 'Older Girls(1-7yrs)',
    'https://www.shein.co.uk/Maternity-c-2985.html?ici=uk_tab03navbar10menu01&scici=navbar_KidsHomePage~~tab03navbar10menu01~~10_1~~real_2985~~~~0&src_module=topcat&src_tab_page_id=page_home1656931976031&src_identifier=fc%3DKids%60sc%3DMATERNITY%60tc%3DVIEW%20ALL%60oc%3D0%60ps%3Dtab03navbar10menu01%60jc%3Dreal_2985&srctype=category&userpath=category-MATERNITY-VIEW-ALL': 'Maternity',
    'https://www.shein.co.uk/Makeup-c-2042.html?ici=uk_tab05navbar01&scici=navbar_BeautyHomePage~~tab05navbar01~~1~~webLink~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657139830891&src_identifier=fc%3DBeauty%60sc%3DMAKEUP%60tc%3D0%60oc%3D0%60ps%3Dtab05navbar01%60jc%3Durl_http%253A%252F%252Fwww.shein.co.uk%252FMakeup-c-2042.html&srctype=category&userpath=category-MAKEUP': 'MAKEUP',
    'https://www.shein.co.uk/Beauty-Tools-c-2041.html?ici=uk_tab05navbar03&scici=navbar_BeautyHomePage~~tab05navbar03~~3~~webLink~~~~0&src_module=topcat&src_tab_page_id=page_real_class1657139766102&src_identifier=fc%3DBeauty%60sc%3DBEAUTY%20TOOLS%60tc%3D0%60oc%3D0%60ps%3Dtab05navbar03%60jc%3Durl_https%253A%252F%252Fwww.shein.co.uk%252FBeauty-Tools-c-2041.html&srctype=category&userpath=category-BEAUTY-TOOLS': 'Beauty Tools',
    'https://www.shein.co.uk/Personal-Care-c-2171.html?ici=uk_tab05navbar05&scici=navbar_BeautyHomePage~~tab05navbar05~~5~~real_2171~~~~0&src_module=topcat&src_tab_page_id=page_home1657139761615&src_identifier=fc%3DBeauty%60sc%3DPERSONAL%20CARE%60tc%3D0%60oc%3D0%60ps%3Dtab05navbar05%60jc%3Dreal_2171&srctype=category&userpath=category-PERSONAL-CARE': 'Personal Care',
    'https://www.shein.co.uk/Wigs-Accs-c-3644.html?ici=uk_tab05navbar04&scici=navbar_BeautyHomePage~~tab05navbar04~~4~~real_3644~~~~0&src_module=topcat&src_tab_page_id=page_home1657139713069&src_identifier=fc%3DBeauty%60sc%3DWIGS%20%26%20ACCS%60tc%3D0%60oc%3D0%60ps%3Dtab05navbar04%60jc%3Dreal_3644&srctype=category&userpath=category-WIGS-ACCS': 'Wigs & Accs',
}

stolb = ['SKU', 'Name', 'Published', 'Is featured?', 'Visibility in catalog', 'Description',
         'Regular price', 'Categories', 'Tags', 'Images', 'Attribute 1 name',
         'Attribute 1 value(s)', 'Attribute 1 visible', 'Attribute 1 global', 'Attribute 2 name',
         'Attribute 2 value(s)', 'Attribute 2 visible', 'Attribute 2 global',
         'Backorders allowed?', 'Sold individually?', 'In stock?']

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
BASE_DIR = Path(__file__).resolve().parent.parent

name = f'Shein_products_{datetime.now().strftime("%Y-%m-%d_%H:%m")}.csv'
with open(f"{name}", 'w') as file:
    writer = csv.writer(file)
    writer.writerow(stolb)
for item in URLS.keys():
    try:
        driver.get(item)
        time.sleep(0.5)
        try:
            driver.find_elements(By.CLASS_NAME, "S-dialog__closebtn")[1].click()
        except Exception as ex:
            pass

        try:
            driver.find_element(By.CLASS_NAME, "side-filter__item-viewMore").click()
        except Exception as ex:
            pass

        soup = BeautifulSoup(driver.page_source, "lxml")

        categories = str(URLS[item]).strip()

        for info in soup.find_all("a", class_="S-product-item__img-container"):
            try:
                # print(info)
                URL = "https://www.shein.co.uk" + info['href']
                driver.get(URL)
                time.sleep(0.2)
                try:
                    driver.find_elements(By.CLASS_NAME, "S-dialog__closebtn")[6].click()
                except Exception as ex:
                    pass

                try:
                    driver.find_element(By.CLASS_NAME, "product-intro__description-head").click()
                except:
                    pass
                soup = BeautifulSoup(driver.page_source, "lxml")

                name_product = soup.find("h1", class_="product-intro__head-name").text.strip()
                price = str(float(soup.find(class_="from").text.strip().replace('GBP£', '')) * (
                        1.00 + (Additional_Percentage_To_The_Price / 100)))
                sizes = []
                try:
                    for i in soup.find_all(class_="product-intro__size-radio-inner"):
                        sizes.append(i.text.strip())
                except:
                    pass
                try:
                    description = {}
                    str_description = ''
                    key = soup.find(class_='product-intro__attr-wrap').find_all(class_='key')
                    val = soup.find(class_='product-intro__attr-wrap').find_all(class_='val')
                    for item_1 in range(len(key)):
                        description[f"{key[item_1].text.strip().replace(':', '')}"] = val[item_1].text.strip()
                        if f'{key[item_1].text.strip().replace(":", "")}:  {val[item_1].text.strip()};\n' not in str_description:
                            str_description += f'{key[item_1].text.strip().replace(":", "")}:  {val[item_1].text.strip()}   '
                except:
                    description = "No description"
                all_photos = []
                images = []
                c = 0
                for item_2 in soup.find_all(class_="swiper-slide"):
                    c += 1
                    a = ("https:" + str(item_2).replace('"/> <!-- --> <!-- --></div>', "").replace(
                        '"/></a> <div class="common-swiperv2__btm"><div class="ori">', '').replace('"/></div>',
                                                                                                   '').split(
                        'src="')[-1])
                    if "img" in a and "webp" and "<" not in a and '>' not in a:
                        all_photos.append(a)
                # print(all_photos)
                number_for_SKU = '123456789'
                SKU = ''
                for i in range(1, 16):
                    SKU += random.choice(number_for_SKU)
                try:
                    with open(f"{name}", 'w') as file:
                        writer = csv.writer(file)
                        writer.writerow([f'{SKU}', f'{name_product}', '1', '0', 'visible', f'{str_description}',
                                         f"{price}", f"{categories}", f"{','.join(categories.split())}",
                                         f'{",".join(all_photos)}', "Color", f"{description['Color']}", '1', '1',
                                         'Size',
                                         f'{",".join(sizes)}', '1', '1', '0', '0', '1'])

                except Exception as ex:
                    pass
            except:
                pass
    except Exception as ex:
        pass
        time.sleep(0.5)

driver.close()
