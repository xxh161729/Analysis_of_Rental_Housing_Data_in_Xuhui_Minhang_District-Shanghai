import requests
from bs4 import BeautifulSoup
import csv
import re


session = requests.Session()
login_url = "https://sh.fang.lianjia.com/loupan/xuhui/#xuhui"
data = {"username": "15363582696", "password": "Abc28221626"}
session.post(login_url, data=data)  # 登录后Cookie自动保存

# 1. 定义请求URL
url = "https://sh.lianjia.com/loupan/xuhui/"

# 2. 定义请求头（从浏览器复制并整理）
headers = {
    "Accept": 
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": 
    "lianjia_uuid=f45e7ece-36e2-4255-8797-92088ca0edd1; _ga=GA1.2.318962193.1747062489; crosSdkDT2019DeviceId=v0347f--p7z7kn-j5i391s8ckkxz6j-i9r4yrfy7; _jzqx=1.1747492384.1747537730.2.jzqsr=google%2Ecom|jzqct=/.jzqsr=sh%2Elianjia%2Ecom|jzqct=/; lfrc_=1ead0e88-08fb-41eb-946c-dd1cd700a6aa; select_city=310000; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1747062478,1747492383,1747537729,1747983225; HMACCOUNT=F5F6302347E31A4E; _jzqa=1.1002995970489272600.1747062478.1747537730.1747983226.4; _jzqc=1; _jzqy=1.1747062478.1747983226.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; _jzqckmp=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22196c509d758f50-0bd495e9a9fea3-26011f51-2073600-196c509d759102f%22%2C%22%24device_id%22%3A%22196c509d758f50-0bd495e9a9fea3-26011f51-2073600-196c509d759102f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E9%93%BE%E5%AE%B6%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysh%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; Hm_lvt_efa595b768cc9dc7d7f9823368e795f1=1747540663,1747983232; Hm_lpvt_efa595b768cc9dc7d7f9823368e795f1=1747983232; _gid=GA1.2.1191431066.1747983232; _qzjc=1; _jzqc=1; lianjia_ssid=5a6eeafd-dfed-4868-8d55-4cca9f36b5a4; login_ucid=2000000483568254; lianjia_token=2.0013688b8b46214c1902c5a2babf990932; lianjia_token_secure=2.0013688b8b46214c1902c5a2babf990932; security_ticket=ad0LhLt9gnx5QxsO3akzdWPDC6ervyR4Weh3Lo4Mdoj30vbOLrwSnNOnQnrQ+J9AMD1008QUMXiHDcM3X/dbISmLByL5fWt+zWbII2kFgLeEtafnnqIIIoXtIDhXk3HKHHJmYQ5JRvRwnOkHnnmjpa+WV/EpDVABcdFm8aCayOY=; ftkrc_=1bcde53b-215a-439c-b0ce-0ac2002ed2c3; _ga_LRLL77SF11=GS2.2.s1747983237$o4$g1$t1747984388$j0$l0$h0; _ga_GVYN2J1PCG=GS2.2.s1747983237$o4$g1$t1747984388$j0$l0$h0; digData=%7B%22key%22%3A%22loupan_index%22%7D; _jzqx=1.1747492384.1747987038.2.jzqsr=google%2Ecom|jzqct=/.jzqsr=sh%2Elianjia%2Ecom|jzqct=/; _jzqa=1.1002995970489272600.1747062478.1747537730.1747983226.4; _ga_00MKBBEWEN=GS2.2.s1747987038$o3$g1$t1747989427$j0$l0$h0; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1747989964; _qzja=1.1595734200.1747540493596.1747983240132.1747987038408.1747989427078.1747989963980.0.0.0.11.3; _qzjb=1.1747987038408.6.0.0.0; _qzjto=10.2.0; _jzqb=1.6.10.1747987038.1; srcid=eyJ0IjoiXCJ7XFxcImRhdGFcXFwiOlxcXCJkYzQ3OGI0MjZiOTFlZDg0ZThjYjUwNGEwYWNjZWRhYzlkMmQxYThkMDNmZjA1ZDcxMDRmMWQ2NDdkOTM2YmFkMG",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"  # 补充User-Agent
}
def get_response(url, headers, session):
    # 3. 发送GET请求
    response = session.get(url, headers=headers,cookies=session.cookies)  # 使用登录后的session对象

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



def extract_property_data(html,data):
    # 假设每个房源信息在class为'property-item'的div中
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    houses = soup.select('ul.resblock-list-wrapper > li.resblock-list')

    
    
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

    

def export_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["房名","房价", "面积", "地点"])
        writer.writeheader()
        writer.writerows(data)

def main():
    properties = []
    for i in range(1,3):
        url = "https://sh.fang.lianjia.com/loupan/xuhui/pg"+str(i)+"/#xuhui"
        html = get_response(url, headers, session)  # 获取页面内容
        extract_property_data(html,properties)
    export_to_csv(properties, 'properties.csv')
    print("数据已保存到 properties.csv")

if __name__ == "__main__":
    main()


