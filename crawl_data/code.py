from rest_framework.utils import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from random import randrange
import requests

from webdriver_manager.chrome import ChromeDriverManager

# setting web driver
# chrome_options = Options()
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--window-size=1920x1080")
# # chrome_options.add_argument("user-data-dir=C:\\Users\\huynh\\AppData\\Local\\Google\\Chrome\\User Data") #Path to your chrome profile
# driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

# setting file
with open('product_list.json', "r", encoding='utf-8') as file:
    input_data = json.loads(file.read())
print(input_data)


#################################################################################
category = 'Laptop'
list_output_data = []
base_url = 'https://phongvu.vn/api/product/'
len_input_data = len(input_data)
cnt = 0
for product in input_data:
    cnt += 1
    print(cnt, '/', len(input_data))
    url = base_url + product['productInfo']['skuId']
    response = requests.get(url)
    response_data = response.json()['result']['product']

    attribute_groups = response_data['productDetail']['attributeGroups']
    spec = ''
    for e in attribute_groups:
        spec += e['name'] + ':' + e['value']

    output_data = {
        'id': response_data['productInfo']['skuId'],
        'name': response_data['productInfo']['name'],
        'description': response_data['productDetail']['seoInfo']['description'],
        'short_description': response_data['productDetail']['seoInfo']['shortDescription'],
        'thumbnail': response_data['productInfo']['imageUrl'],
        'sale_price': response_data['prices'][0]['latestPrice'],
        'price': response_data['prices'][0]['sellPrice'],
        'brand': response_data['productInfo']['brand']['name'],
        'category': category,
        'specifications': spec,
        'images': response_data['productDetail']['images'],
    }
    list_output_data.append(output_data)
    time.sleep(1)


f = open('data.json', "w", encoding='utf-8')
f.write(json.dumps(list_output_data))
f.close()
print("Saved data to data.json")
exit()
#
# # open url
# driver.get('https://www.facebook.com/DUTpage')
# time.sleep(1)
#
# # scroll down x times
# for _ in range(5):
#     try:
#         btn_hide = driver.find_element_by_id('expanding_cta_close_button')
#         btn_hide.click()
#     except Exception as e:
#         print(str(e))
#     time.sleep(randrange(1, 3))
#     driver.execute_script("window.scrollBy(0, 400)")
#
# # list_post = driver.find_elements_by_class_name('userContentWrapper')
# list_post = driver.find_elements_by_xpath("//span[contains(text(), 'My Button')]")
#
# for element in list_post:
#     try:
#         btn_hide.click()
#     except Exception as e:
#         print(str(e))
#
#     driver.execute_script("arguments[0].scrollIntoView();", element)
#     try:
#         btn_more_info = element.find_element_by_class_name('see_more_link')
#         btn_more_info.click()
#     except Exception as e:
#         print(str(e))
#
#     try:
#         btn_more_cmt = element.find_element_by_class_name('_4ssp')
#         btn_more_cmt.click()
#     except Exception as e:
#         print(str(e))
#
#     print('-----------------------------')
#     print(element.find_element_by_class_name('timestampContent').text)
#     print(element.find_element_by_class_name('userContent').text)
#     print('Comment')
#     try:
#         cmt_area = element.find_element_by_class_name('_7a9a')
#         btn_more_cmt_list = cmt_area.find_elements_by_class_name('_5v47')
#         for e in btn_more_cmt_list:
#             e.click()
#         print(cmt_area.text)
#     except Exception as e:
#         print(str(e))
#     print('-----------------------------')
#
#     f.writelines('-----------------------------\n')
#     f.writelines(element.text + '\n')
#     f.writelines('-----------------------------\n')
#
# f.close()
