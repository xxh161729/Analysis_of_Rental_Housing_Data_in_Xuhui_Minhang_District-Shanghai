import requests
from bs4 import BeautifulSoup
import time
import random
import json
from fake_useragent import UserAgent

ua = UserAgent()
base_url = "https://sh.lianjia.com/ershoufang/minhang/pg{}/"
headers = {
    'Referer': 'https://sh.lianjia.com/ershoufang/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1'
}

def get_page_data(page):
    url = base_url.format(page)
    try:
        
        delay = random.uniform(10, 15) + random.random() 
        time.sleep(delay)

        headers['User-Agent'] = ua.random 
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"请求异常：{e}")
        return None

def parse_html(html):
    if not html:
        return []
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('li', class_='clear LOGCLICKDATA')
    result = []
    for item in items:
        try:
            title_elem = item.find('a', class_='VIEWDATA CLICKDATA maidian-detail')
            title = title_elem.get_text(strip=True) if title_elem else '无标题'

            total_price_elem = item.find('div', class_='totalPrice totalPrice2')
            total_price = total_price_elem.get_text(strip=True) if total_price_elem else '0'

            unit_price_elem = item.find('div', class_='unitPrice')
            unit_price = unit_price_elem.get('data-price') if unit_price_elem else '0'

            house_info_elem = item.find('div', class_='houseInfo')
            house_info = house_info_elem.get_text(strip=True) if house_info_elem else ''

            result.append({
                '标题': title,
                '总价(万)': total_price,
                '单价(元/平米)': unit_price,
                '房屋信息': house_info
            })
        except Exception as e:
            print(f"解析异常: {str(e)}")
            continue  
    return result

def parse_new_house_html(html):
    if not html:
        return []
    soup = BeautifulSoup(html, 'lxml')
    result = []
    house_items = soup.find_all('li', class_='resblock-list post_ulog_exposure_scroll has-results')
    for item in house_items:
        try:
            name_elem = item.find('a', class_='name')
            name = name_elem.get_text(strip=True) if name_elem else '无名称'

            type_elem = item.find('span', class_='resblock-type')
            house_type = type_elem.get_text(strip=True) if type_elem else '无类型'

            status_elem = item.find('span', class_='sale-status')
            sale_status = status_elem.get_text(strip=True) if status_elem else '未知状态'

            location_elems = item.find('div', class_='resblock-location').find_all('span')
            district = location_elems[0].get_text(strip=True) if len(location_elems) > 0 else ''
            sub_district = location_elems[2].get_text(strip=True) if len(location_elems) > 2 else ''

            main_price_elem = item.find('span', class_='number')
            average_price = main_price_elem.get_text(strip=True) if main_price_elem else '0'

            second_price_elem = item.find('div', class_='second')
            total_price = second_price_elem.get_text(strip=True).replace('总价', '').replace('(万/套)', '') if second_price_elem else '0'

            result.append({
                '楼盘名称': name,
                '楼盘类型': house_type,
                '销售状态': sale_status,
                '区域': district,
                '子区域': sub_district,
                '均价(元/㎡)': average_price,
                '总价(万/套)': total_price
            })
        except Exception as e:
            print(f"解析异常: {str(e)}")
            continue 
    return result

def main():
    all_data = [] 
    max_page = 20
    for page in range(1, max_page + 1):
        print(f"正在爬取第 {page} 页...")
        html = get_page_data(page)
        if html:
            page_data = parse_new_house_html(html)
            if page_data:
                all_data.extend(page_data)
                print(f"第 {page} 页解析成功，累计 {len(all_data)} 条数据")
            else:
                print(f"第 {page} 页无有效数据")
        else:
            print(f"第 {page} 页爬取失败，终止爬取")
            break

    if not all_data:
        print("没有有效数据可保存")
    else:
        save_to_json(all_data)
        print(f"全部完成！共保存 {len(all_data)} 条数据到 JSON 文件")

def save_to_json(data, filename='二手房链家.json'):
    """保存数据到 JSON 文件"""
    try:
        existing_data = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            print(f"成功读取现有文件 {filename}，已有 {len(existing_data)} 条数据")
        except FileNotFoundError:
            print(f"文件 {filename} 不存在，将创建新文件")

        if not data:
            print("传入的数据为空，不进行保存操作")
            return
        existing_data.extend(data)
        print(f"合并后共有 {len(existing_data)} 条数据")

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        print(f"数据已成功保存到 {filename}")

    except Exception as e:
        print(f"保存文件失败：{e}")

if __name__ == '__main__':
    main() 

