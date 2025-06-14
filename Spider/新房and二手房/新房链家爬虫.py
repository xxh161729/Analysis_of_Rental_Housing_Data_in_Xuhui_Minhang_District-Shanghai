import requests
import time
import random
import json



api_url = "https://sh.fang.lianjia.com/loupan/ah100017532/"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    'Referer': 'https://sh.fang.lianjia.com/loupan/minhang/',
    "Host":"sh.fang.lianjia.com",
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie' : 
    r"lianjia_uuid=f45e7ece-36e2-4255-8797-92088ca0edd1; _ga=GA1.2.318962193.1747062489; crosSdkDT2019DeviceId=v0347f--p7z7kn-j5i391s8ckkxz6j-i9r4yrfy7; _jzqx=1.1747492384.1747537730.2.jzqsr=google%2Ecom|jzqct=/.jzqsr=sh%2Elianjia%2Ecom|jzqct=/; lfrc_=1ead0e88-08fb-41eb-946c-dd1cd700a6aa; select_city=310000; session_id=0bda86be-eef5-7809-a473-a385d434eb1e; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1747062478,1747492383,1747537729,1747983225; HMACCOUNT=F5F6302347E31A4E; _jzqa=1.1002995970489272600.1747062478.1747537730.1747983226.4; _jzqc=1; _jzqy=1.1747062478.1747983226.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; _jzqckmp=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22196c509d758f50-0bd495e9a9fea3-26011f51-2073600-196c509d759102f%22%2C%22%24device_id%22%3A%22196c509d758f50-0bd495e9a9fea3-26011f51-2073600-196c509d759102f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E9%93%BE%E5%AE%B6%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysh%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; Hm_lvt_efa595b768cc9dc7d7f9823368e795f1=1747540663,1747983232; Hm_lpvt_efa595b768cc9dc7d7f9823368e795f1=1747983232; _gid=GA1.2.1191431066.1747983232; _qzjc=1; _jzqc=1; lianjia_ssid=5a6eeafd-dfed-4868-8d55-4cca9f36b5a4; login_ucid=2000000483568254; lianjia_token=2.0013688b8b46214c1902c5a2babf990932; lianjia_token_secure=2.0013688b8b46214c1902c5a2babf990932; security_ticket=ad0LhLt9gnx5QxsO3akzdWPDC6ervyR4Weh3Lo4Mdoj30vbOLrwSnNOnQnrQ+J9AMD1008QUMXiHDcM3X/dbISmLByL5fWt+zWbII2kFgLeEtafnnqIIIoXtIDhXk3HKHHJmYQ5JRvRwnOkHnnmjpa+WV/EpDVABcdFm8aCayOY=; ftkrc_=1bcde53b-215a-439c-b0ce-0ac2002ed2c3; _ga_LRLL77SF11=GS2.2.s1747983237$o4$g1$t1747984388$j0$l0$h0; _ga_GVYN2J1PCG=GS2.2.s1747983237$o4$g1$t1747984388$j0$l0$h0; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1747987038; digData=%7B%22key%22%3A%22loupan_index%22%7D; _qzja=1.1595734200.1747540493596.1747983240132.1747987038408.1747983557093.1747987038408.0.0.0.6.3; _qzjto=5.2.0; _jzqa=1.1002995970489272600.1747062478.1747537730.1747987038.4; _jzqx=1.1747492384.1747987038.2.jzqsr=google%2Ecom|jzqct=/.jzqsr=sh%2Elianjia%2Ecom|jzqct=/; srcid=eyJ0IjoiXCJ7XFxcImRhdGFcXFwiOlxcXCJkYzQ3OGI0MjZiOTFlZDg0ZThjYjUwNGEwYWNjZWRhYzlkMmQxYThkMDNmZjA1ZDcxMDRmMWQ2NDdkOTM2YmFkMGEwNjM5YTgyZDkzZjU1ODkxNzZkNzZlOGUxNWYzOTNkNThkNWFlMDNmZjYzNzc0ZmE0MGFiYjM4Y2I4YjExYjI2NmMwOTFlOWM5NWNhODViNmVkNjE4YmZkZDU2MzZkZDIxZmIzNDk0MDdjYTNiMTI2YTIxOTFmOTRmMDExN2FkNGZjZjk5NzUzZDFiMDZhNzhmNTgwMDljZTVlZWViYzc2YTkzNDIxZjk0MDY4MzViMWYzYTIwY2U4ZDE3MjE2XFxcIixcXFwia2V5X2lkXFxcIjpcXFwiMVxcXCIsXFxcInNpZ25cXFwiOlxcXCI5YWUwZjFjNFxcXCJ9XCIiLCJyIjoiaHR0cHM6Ly9zaC5mYW5nLmxpYW5qaWEuY29tL2xvdXBhbi8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; _jzqb=1.1.10.1747987038.1; _qzjb=1.1747987038408.1.0.0.0; _ga_00MKBBEWEN=GS2.2.s1747987038$o3$g0$t1747987038$j0$l0$h0; lj_newh_session=eyJpdiI6IlFKNk9cL2s2NE85SWlzaVJUWGNQU0FBPT0iLCJ2YWx1ZSI6Ilg3VE5vVmhZcXV6bUg4eHBtOWxIUjdvR0xlUndBb2dpcmhEcytpSlhXV3JMNzY0c1ZrUklJXC9wNThmeFQ1cit0RnIyVWdZQXJFcFNJR3d5OXZWSmcxQT09IiwibWFjIjoiYjg2MmVlZGEzYzhmY2JjM2UzZWUzZjA5NjQzYjg0NWViZjQzMDJmMjc5MGMzMmRjMGIwNDlmYjJiODAxNzY5MyJ9"}

def get_page_data(page):
    params = {
        '_t': 1,
        'page': page,
        'page_size': 12,
        'new_code': '',
        'city_id': '310000',
        'condition': r'sa%2Fminhang',
        'kw': '',
    }
    
    try:
        response = requests.get(
            api_url,
            params=params,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            with open("lianjia.html","w",encoding="utf-8") as f:
                f.write(response.text)
                print("保存成功")
            return response.json()
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"请求异常：{e}")
        return None

def parse_json_data(json_data):
    result = []
    try:
        for item in json_data['data']['list']:
            price_info = item.get('price_show', {})
            price_str = f"{price_info.get('price', '')}{price_info.get('price_unit', '')}"

            area_range = item.get('area_interval', {})
            area_str = f"{area_range.get('min_area', '')}-{area_range.get('max_area', '')}㎡"
            
            result.append({
                '楼盘名称': item['name'],
                '楼盘类型': item['resblock_type'],
                '销售状态': item['sale_status'],
                '区域': item['district'],
                '详细地址': item['address'],
                '均价': price_str,
                '户型面积': area_str,
                '开盘时间': item.get('open_time', '待定'),
                '开发商': item.get('developer', '未知'),
                '在售户型': [x['desc'] for x in item.get('room_types', [])]
            })
        return result
    except Exception as e:
        print(f"解析异常：{e}")
        return []


if __name__ == '__main__':
    all_data = []
    max_page = 3
    
    for page in range(1, max_page + 1):
        print(f"正在获取第 {page} 页...")
        json_data = get_page_data(page)

        time.sleep(3)
        
        if json_data and json_data.get('success'):
            page_data = parse_json_data(json_data)
            if page_data:
                all_data.extend(page_data)
                print(f"第 {page} 页成功获取 {len(page_data)} 条数据")
            else:
                print(f"第 {page} 页无有效数据")
        else:
            print(f"第 {page} 页获取失败")
            break

    if all_data:
        with open('lianjia_newhouse.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"成功保存 {len(all_data)} 条数据")
    else:
        print("未获取到有效数据")

