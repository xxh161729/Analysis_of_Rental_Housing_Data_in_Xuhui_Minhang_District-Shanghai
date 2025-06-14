import requests
import json
import time


def fetch_subway_data():
    """
    爬取高德地铁所有站点的经纬度数据
    返回包含所有站点信息的列表
    """
    # 目标URL - 获取全国所有城市的地铁数据
    url = "https://map.amap.com/service/subway?_1748605888942&srhdata=3100_drw_shanghai.json"
    
    # 设置请求头部，模拟浏览器访问
    headers = {
        "Referer": "https://map.amap.com/subway/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive"
    }
    
    try:
        # 发送HTTP GET请求
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析返回的JSON数据
        data = response.json()
        
        # 创建存储所有站点数据的列表
        all_stations = []
        

        for line in data["l"]:
            line_name = line["ln"]
            line_id = line["ls"]
            
            # 遍历线路的所有站点
            for station in line["st"]:
                # 检查站点是否有有效坐标
                if "sl" not in station or not station["sl"]:
                    continue
                
                # 提取经纬度并转换格式
                lon, lat = station["sl"].split(",")
                
                station_data = {
                    "line_id": line_id,
                    "line_name": line_name,
                    "station_id": station.get("si", ""),
                    "station_name": station["n"],
                    "longitude": float(lon),
                    "latitude": float(lat),
                    "poi_id": station.get("poiid", ""),
                    "is_transfer": "su" in station and station["su"] == "1"
                }
                all_stations.append(station_data)
        
        return all_stations
    
    except Exception as e:
        print(f"爬取数据时出错: {e}")
        return []

def save_to_json(data, filename):
    """将数据保存为JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已成功保存至 {filename}")
    except Exception as e:
        print(f"保存文件时出错: {e}")


if __name__ == "__main__":
    print("开始爬取高德地铁站点数据...")
    start_time = time.time()
    
    # 获取地铁站点数据
    subway_data = fetch_subway_data()
    
    if not subway_data:
        print("未能获取有效的地铁站点数据")
        exit(1)
    
    print(f"共爬取到 {len(subway_data)} 个地铁站点数据")
    
    # 保存数据到JSON文件
    save_to_json(subway_data, "subway_stations.json")
    
    # 计算执行时间
    elapsed_time = time.time() - start_time
    print(f"爬取完成! 总耗时: {elapsed_time:.2f} 秒")