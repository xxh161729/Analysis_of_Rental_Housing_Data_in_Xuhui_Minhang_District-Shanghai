import json
import requests
import time
# 高德API配置
AMAP_KEY = "d03c7b27db05d88ad9d10d9c64353130"  # 替换成你的Key
GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"

def get_geocode(address):
    """调用高德地理编码API获取经纬度"""
    params = {
        "key": AMAP_KEY,
        "address": address,
        "city": "上海市" 
    }
    response = requests.get(GEOCODE_URL, params=params)
    data = response.json()
    
    if data["status"] == "1" and data["count"] != "0":
        location = data["geocodes"][0]["location"]  # 格式："经度,纬度"
        lng, lat = location.split(",")
        return {"lng": float(lng), "lat": float(lat)}
    else:
        print(f"地址解析失败: {address}")
        print(f"错误信息: {data['info']}")
        return None

# 读取原始JSON文件
with open("数据\链家租房闵行数据.json", "r", encoding="utf-8") as f:
    rent_data = json.load(f)
success = 0
# 处理每条租房信息
for item in rent_data:
    # 拼接完整地址（示例：上海市徐汇区万体馆银星名庭）
    if item["片区"] != '':
        area_parts = item["片区"].split("-")
        full_address = f"上海市徐汇区{area_parts[1]}{area_parts[2]}"  # 徐汇区-万体馆-银星名庭
    else:
        continue  # 如果片区信息缺失，则跳过该条数据
    
    # 获取经纬度
    location = get_geocode(full_address)
    if location:
        item["location"] = location
        success += 1
    time.sleep(0.8)
# 保存带经纬度的新文件
with open("数据\MinHang_rent_data.json", "w", encoding="utf-8") as f:
    json.dump(rent_data, f, ensure_ascii=False, indent=4)
print(success, "条数据成功添加经纬度信息。")