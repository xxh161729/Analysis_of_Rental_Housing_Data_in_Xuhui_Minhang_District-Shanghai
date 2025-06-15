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
    
valid_data = []
success = 0
# 读取原始JSON文件
for data in ["数据\JSON\闵行租房_raw.json","数据\JSON\链家租房数据徐汇_raw.json"]:
    with open(data, "r", encoding="utf-8") as f:
        rent_data = json.load(f)
    
    # 处理每条租房信息
    for item in rent_data:
        # 拼接完整地址（示例：上海市徐汇区万体馆银星名庭）
        if item["片区"] == '':
            continue

        area_parts = item["片区"].split("-")
        full_address = f"上海市{area_parts[0]}区{area_parts[1]}{area_parts[2]}"  # 徐汇区-万体馆-银星名庭
        
        # 获取经纬度
        location = get_geocode(full_address)
        if location:
            item["lng"] = location["lng"]
            item["lat"] = location["lat"]
            item["区域"] = area_parts[0]
            valid_data.append(item)
            success += 1
            # print(success)
        time.sleep(0.9)

# 保存带经纬度的新文件
with open("cleaned_data.json", "w", encoding="utf-8") as f:
    json.dump(valid_data, f, ensure_ascii=False, indent=2)


# 打印统计信息
valid_count = len(valid_data)
print(f"成功添加经纬度数据量：{success}")
print(f"最终有效数据量：{valid_count}")