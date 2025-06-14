import requests
from bs4 import BeautifulSoup
import csv
import re


session = requests.Session()
login_url = "https://sh.lianjia.com/ershoufang/minhang"
data = {"username": "15363582696", "password": "Abc28221626"}
session.post(login_url, data=data)  # 登录后Cookie自动保存

# 1. 定义请求URL
url = "https://sh.lianjia.com/ershoufang/minhang"

# 2. 定义请求头（从浏览器复制并整理）
headers = {
    # "Accept": 
    # "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": 
    r"SECKEY_ABVK=4Tzaee5XKPlff2caW5AqucbpCpz4P5nkqaScyv4Hj18%3D; BMAP_SECKEY=7Cm6MnMB1OYyjkZHQWwYeH1Toid1oPa7gQ13cM-EwOamJMUmsq1ThFVWodc83f_uS3M6pHEnW6Xvu9lUPxBRdNLFDd7vh44vDTWX6cbXLeoAukRMm5n2Xim56siSZ8JIacZenq1bWPZai3n3aMTLs9A33H2OngZ2-vDRJkyIax7LGJMS7MArGqHpQxR9TA08; lianjia_uuid=f45e7ece-36e2-4255-8797-92088ca0edd1; _ga=GA1.2.318962193.1747062489; crosSdkDT2019DeviceId=v0347f--p7z7kn-j5i391s8ckkxz6j-i9r4yrfy7; lfrc_=1ead0e88-08fb-41eb-946c-dd1cd700a6aa; select_city=310000; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1747062478,1747492383,1747537729,1747983225; HMACCOUNT=F5F6302347E31A4E; _jzqc=1; _jzqy=1.1747062478.1747983226.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; _jzqckmp=1; _qzjc=1; Hm_lvt_efa595b768cc9dc7d7f9823368e795f1=1747540663,1747983232; Hm_lpvt_efa595b768cc9dc7d7f9823368e795f1=1747983232; _gid=GA1.2.1191431066.1747983232; login_ucid=2000000483568254; lianjia_token=2.0013688b8b46214c1902c5a2babf990932; lianjia_token_secure=2.0013688b8b46214c1902c5a2babf990932; security_ticket=ad0LhLt9gnx5QxsO3akzdWPDC6ervyR4Weh3Lo4Mdoj30vbOLrwSnNOnQnrQ+J9AMD1008QUMXiHDcM3X/dbISmLByL5fWt+zWbII2kFgLeEtafnnqIIIoXtIDhXk3HKHHJmYQ5JRvRwnOkHnnmjpa+WV/EpDVABcdFm8aCayOY=; ftkrc_=1bcde53b-215a-439c-b0ce-0ac2002ed2c3; _ga_00MKBBEWEN=GS2.2.s1747987038$o3$g1$t1747989427$j0$l0$h0; _jzqa=1.1002995970489272600.1747062478.1747983226.1748003301.5; _jzqx=1.1747492384.1748003301.3.jzqsr=google%2Ecom|jzqct=/.jzqsr=sh%2Efang%2Elianjia%2Ecom|jzqct=/; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22196c509d758f50-0bd495e9a9fea3-26011f51-2073600-196c509d759102f%22%2C%22%24device_id%22%3A%22196c509d758f50-0bd495e9a9fea3-26011f51-2073600-196c509d759102f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysh%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; GUARANTEE_POPUP_SHOW=true; GUARANTEE_BANNER_SHOW=true; _ga_LRLL77SF11=GS2.2.s1748003313$o5$g1$t1748006887$j0$l0$h0; _ga_GVYN2J1PCG=GS2.2.s1748003313$o5$g1$t1748006887$j0$l0$h0; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1748007667; _qzja=1.1512830283.1747062478126.1747983225801.1748003301214.1748006875905.1748007667476.0.0.0.60.5; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMGM0ZmQ5ODFjN2VkMTNkOGVjMzZjNGFiODIyMzIxNWZkMWE2MDllMGU3ODJlY2JkYzE0ODU5ZjI3ZWVkMzgyZDZkZDQxMGMzMjQ2ODM2YTIxNzI4MjBhNjQ2OWVmNGYwYzRhZmQxMjZlMjAyNjc4OWY4MTVhMGZjNTFkNDY1ZWU4ZmM5OGFhYjRiYThhODAzNmJjNmU0ZDAxZmVkMTIyNDQ1MmEyM2E2MGUyZGU2MzAxMTFhMjJlOTlmNjRiNGVjOGEyZWU5ZjFjYzNjODgwZWVhMWM1OWRiZDZmOTk4NDY2ZTQ1Zjk0OTZjNzViNzllNmY3MDc2OWU0Y2Y4MWNhYVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI0NWMxNmMwYlwifSIsInIiOiJodHRwczovL3NoLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvbWluaGFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; lianjia_ssid=f0e184f6-437d-4a41-ab49-a3b1b826b501",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"  # 补充User-Agent
}

def get_response(url, headers, cookie):
    # 3. 发送GET请求
    response = session.get(url, headers=headers,cookies=cookie)  # 使用登录后的session对象

    html = None

    # 4. 检查响应状态码和内容
    if response.status_code == 200:
        html = response.text
        if html is not None:
            print("请求成功，正在解析数据...")
            return html
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print("可能原因：Cookie已过期或触发反爬机制。")
        exit(0)



def extract_property_data(html):
    # 假设每个房源信息在class为'property-item'的div中
    soup = BeautifulSoup(html, 'html.parser')
    houses = soup.select('ul.resblock-list-wrapper > li.resblock-list')

    
    data = []
    for house in houses:
        # 3. 提取房名
        name_tag = house.select_one('.resblock-name h2 a')
        name = name_tag.get_text(strip=True) if name_tag else "N/A"

        # 4. 提取房价
        price_tag = house.select_one('.main-price .number')
        price = price_tag.get_text(strip=True) if price_tag else "价格待定"

        # 5. 提取面积
        area_tag = house.select_one('.resblock-area span')
        area = re.search(r'\d+', area_tag.get_text(strip=True)).group() + '㎡' if area_tag and area_tag.get_text(strip=True) else "N/A"

        # 6. 提取地点
        location_tags = house.select('.resblock-location span, .resblock-location a')
        location_parts = [tag.get_text(strip=True) for tag in location_tags]
        location = ' '.join(location_parts) if location_parts else "N/A"

        data.append({
            "房名": name,
            "房价": price,
            "面积": area,
            "地点": location
        })

    return data



def get_ershoufang_data(html,data):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    # 定位所有房源列表项
    house_list = soup.find_all('li', class_='clear LOGCLICKDATA')

    
    for house in house_list:
        # 提取标题
        title = house.find('div', class_='title').a.text.strip()
        
        # 提取地点（小区名 + 区域）
        position = house.find('div', class_='positionInfo')
        community = position.find_all('a')[0].text.strip()
        area = position.find_all('a')[1].text.strip()
        location = f"{community} - {area}"
        
        # 提取总价
        total_price = house.find('div', class_='totalPrice').span.text.strip()
        
        # 提取均价（去除单位）
        unit_price = house.find('div', class_='unitPrice').span.text.strip()
        unit_price = re.search(r'\d+', unit_price.replace(',', '')).group()
        
        # 提取面积（从户型信息中解析）
        house_info = house.find('div', class_='houseInfo').text
        area_match = re.search(r'(\d+\.\d+)平米', house_info)
        area = area_match.group(1) if area_match else "N/A"
        
        data.append(
            {'标题': title, '地点': location, '总价(万)': total_price, '均价(元/平)': unit_price, '面积(平米)': area}
        )
    



def export_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["房名","房价", "面积", "地点"])
        writer.writeheader()
        writer.writerows(data)

def main():
    properties = []
    # for i in range(1,4):
    url = "https://sh.lianjia.com/ershoufang/minhang/pg"+str(1)
    html = get_response(url, headers, session.cookies)  # 获取页面内容

    get_ershoufang_data(html,properties)

    export_to_csv(properties, '二手房数据.csv')
    print("数据已保存到 二手房.csv")

if __name__ == "__main__":
    main()