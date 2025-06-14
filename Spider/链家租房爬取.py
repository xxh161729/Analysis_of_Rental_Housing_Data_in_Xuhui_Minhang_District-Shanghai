import requests
from bs4 import BeautifulSoup
import time
import random
import json
from fake_useragent import UserAgent
from urllib.robotparser import RobotFileParser

ua = UserAgent()
base_url = "https://sh.lianjia.com/zufang/minhang/rco11/pg{}//"
headers = {
    'Referer': 'https://sh.lianjia.com/zufang/',
    'Cookie': 'ftkrc_', 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1'
}

rp = RobotFileParser()
rp.set_url('https://sh.lianjia.com/robots.txt')
try:
    rp.read()
except Exception as e:
    print(f"读取 robots.txt 失败: {e}")


def get_page_data(page):
    url = base_url.format(page)
    # 检查是否允许访问
    if not rp.can_fetch('*', url):
        print(f"robots.txt 不允许访问 {url}")
        return None
    try:
        # 延长请求间隔至15-20秒，并添加随机抖动
        delay = random.uniform(15, 20) + random.random()  # 增加随机性
        time.sleep(delay)

        headers['User-Agent'] = ua.random  # 每次请求生成新的User-Agent
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            # 打印响应内容，用于调试
            print(f"第 {page} 页响应内容：{response.text}")
            return response.text
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"请求异常：{e}")
        return None


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='content__list--item')
    result = []
    for item in items:
        try:
            # 提取标题
            title_elem = item.find('a', class_='content__list--item--aside')
            title = title_elem['title'] if title_elem else '无标题'

            # 提取价格
            price_elem = item.find('span', class_='content__list--item-price')
            price = price_elem.get_text(strip=True).replace('元/月', '') if price_elem else '0'

            # 提取片区信息（关键修改）
            area_info_elem = item.find('p', class_='content__list--item--des')
            district = ''
            if area_info_elem:
                # 精确提取所有层级的<a>标签，忽略非链接文本
                district_links = area_info_elem.find_all('a', href=True)
                districts = [link.get_text(strip=True) for link in district_links]
                district = '-'.join(districts) if districts else ''
                print(f"Debug - 片区信息: {district}")  # 调试输出

            # 提取面积（优化匹配逻辑）
            area = ''
            if area_info_elem:
                area_text = area_info_elem.get_text(strip=True)
                # 使用正则表达式精确匹配"XX.XX㎡"格式
                import re
                area_match = re.search(r'\d+\.?\d*㎡', area_text)
                area = area_match.group() if area_match else '未知面积'
                print(f"Debug - 面积信息: {area}")  # 调试输出

            result.append({
                '标题': title,
                '价格(元/月)': price,
                '面积': area,
                '片区': district
            })
        except Exception as e:
            print(f"解析异常: {str(e)}")
            continue  # 跳过当前项
    return result


def save_to_json(data, filename='链家租房数据.json'):
    """保存数据到JSON文件"""
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

        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        print(f"数据已成功保存到 {filename}")

    except Exception as e:
        print(f"保存文件失败：{e}")


def main():
    all_data = [] 
    max_page = 50

    for page in range(1, max_page + 1):
        print(f"正在爬取第 {page} 页...")
        html = get_page_data(page)
        if html:
            page_data = parse_html(html)
            if page_data:
                all_data.extend(page_data)
                print(f"第 {page} 页解析成功，累计 {len(all_data)} 条数据")
            else:
                print(f"第 {page} 页无有效数据")
        else:
            print(f"第 {page} 页爬取失败，终止爬取")
            # 可选择不终止，继续尝试下一页
            # continue
            break

    #最后一次保存全部数据
    if not all_data:
        print("没有有效数据可保存")
    else:
        save_to_json(all_data)
        print(f"全部完成！共保存 {len(all_data)} 条数据到JSON文件")


if __name__ == '__main__':
    main()
