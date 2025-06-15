
# 基于链家租房数据的上海市闵行区与徐汇区房价空间可视化分析

## 📌 摘要
通过Python爬虫采集链家网2700左右条租房数据，结合GIS与热力图技术，分析地铁站点对房价的影响。关键技术：
- 反爬策略：Robots协议检查、动态User-Agent轮换、随机延迟
- 数据解析：结构化提取价格/面积/片区等字段
- 空间建模：构建"地铁站距离-房价梯度模型"

## 🎯 项目价值
解决租房决策核心问题：
```diff
+ 量化地铁站点周边租金衰减规律
+ 识别跨区性价比最优居住区域
+ 提供数据驱动的租房策略
```

## 🕷️ 数据爬取
### 链家租房数据
- **目标URL**：  
  `https://sh.lianjia.com/zufang/minhang/`  
  `https://sh.lianjia.com/zufang/xuhui/`
- **爬取框架**：
### 核心功能
```python
# 1. 数据爬取
def get_page(page):
    """获取单页HTML"""
    url = base_url.format(page)
    if not rp.can_fetch('*', url): return None  # 遵守robots.txt
    time.sleep(random.uniform(15, 20))          # 随机延迟防封禁
    headers['User-Agent'] = ua.random           # 动态User-Agent
    response = requests.get(url, headers=headers)
    return response.text if response.ok else None

# 2. 数据解析
def parse_html(html):
    """提取房源关键信息"""
    for item in soup.find_all('div', class_='content__list--item'):
        title = item.find('a')['title']           # 房源标题
        price = item.find('span').text.replace('元/月', '')  # 月租价格
        district = '-'.join([a.text for a in item.find_all('a')])  # 三级片区
        area = re.search(r'\d+\.?\d*㎡', item.text).group()  # 使用面积
        # ... 构建结构化数据字典 ...

# 3. 数据存储
def save_data(data):
    """保存为JSON文件"""
    with open('链家租房数据.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```
### 地铁站点数据
<!-- ![地铁数据采集流程](media/image6.png) -->
- **数据源**：高德地图Ajax请求逆向分析（367个站点）
- **关键字段**：
  ```json
  {
    "line_name": "1号线",
    "station_name": "莘庄",
    "longitude": 121.3852,
    "latitude": 31.1129,
    "is_transfer": false
  }
  ```

## 🧹 数据预处理
### 地理编码流程
```mermaid
graph TD
    A[原始数据] --> B{地址标准化}
    B -->|成功| C[高德Geocoding API]
    B -->|失败| D[人工校验]
    C --> E[经纬度坐标]
```
### 关键计算
- **Haversine距离公式**：
  ```math
  d = 2R \cdot \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos\phi_1\cos\phi_2\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)
  ```
- **衍生变量**：
  - `单价 = 月租金 / 面积`
  - `最近地铁站距离`
## 最终数据样式
![数据样式](media\datasample.png)
## 📊 可视化分析
### 核心图表
| 分析维度 | 可视化展示 |
|---------|------------|
| 价格分布 | ![直方图](media/price.png) | 
| 到最近地铁站距离 | ![直方图](media/Distance.png) | 
| 热力图 | ![热力图](media/heatmap.png) |
| 地铁溢价 | ![散点图](media/regression.png) | 
| 价格区间 | ![饼图](media/piechart.png) | 
| 箱型图 | ![箱型图](media/boxchart.png) |




## 📂 数据文件
- `数据\CSV\house_data.csv`（闵行和徐汇区租房数据）
- `数据\JSON\subway_stations.json`（地铁站点地理数据）
- `Heatmap\data.js`（热力图数据）

## ⚠️ 注意事项
1. 热力图使用对数权重：`weight = log(price)-6`
2. 地铁距离计算含地球曲率修正
3. 数据采集时间：2025年6月

## 尚未完成
新房数据

---
> 📊 完整分析代码见：[Github仓库链接]  