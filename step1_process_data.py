import geopandas as gpd
import json
import os


def process_data():
    # 请确保这里的文件路径正确
    shapefile_path = r"Guangdong-city-2020-shapefile/Guangdong-city-2020.shp"
    print("1. 读取地图数据...")

    try:
        gdf = gpd.read_file(shapefile_path, encoding='gbk')
    except:
        print("错误：无法读取文件，请检查路径")
        return

    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.rename(columns={'市': 'name'})

    # --- 1. 定义文化 (修正版：茂名加入广府) ---
    def define_culture(city_name):
        guangfu = [
            '广州市', '佛山市', '肇庆市', '珠海市', '中山市', '江门市',
            '东莞市', '深圳市', '云浮市', '阳江市', '清远市', '湛江市',
            '茂名市'  # <--- 已修正
        ]
        chaoshan = ['潮州市', '汕头市', '揭阳市', '汕尾市']
        hakka = ['梅州市', '河源市', '惠州市', '韶关市']

        if city_name in guangfu: return "广府"
        if city_name in chaoshan: return "潮汕"
        if city_name in hakka: return "客家"
        return "其他"

    gdf['culture'] = gdf['name'].apply(define_culture)

    # --- 2. 过滤数据 ---
    target_cultures = ['广府', '潮汕', '客家']
    valid_gdf = gdf[gdf['culture'].isin(target_cultures)].copy()

    # --- 3. 计算基础布局 (供参考) ---
    print("2. 计算布局参数...")
    g_minx, g_miny, g_maxx, g_maxy = valid_gdf.total_bounds
    g_width = g_maxx - g_minx
    g_height = g_maxy - g_miny
    global_aspect_ratio = g_width / g_height

    # --- 4. 生成分块数据 ---
    zones_gdf = valid_gdf.dissolve(by='culture')

    layout_config = {
        "aspect_ratio": global_aspect_ratio,
        "zones": {}
    }
    export_map_data = {}

    for culture, row in zones_gdf.iterrows():
        # 计算自动布局参数 (会被之后的手动校准覆盖，但为了完整性保留)
        z_minx, z_miny, z_maxx, z_maxy = row.geometry.bounds
        z_width = z_maxx - z_minx
        z_height = z_maxy - z_miny

        layout_config["zones"][culture] = {
            "style": {
                "left": f"{(z_minx - g_minx) / g_width * 100:.6f}%",
                "top": f"{(g_maxy - z_maxy) / g_height * 100:.6f}%",
                "width": f"{z_width / g_width * 100:.6f}%",
                "height": f"{z_height / g_height * 100:.6f}%"
            }
        }

        # 导出地图数据
        sub_gdf = valid_gdf[valid_gdf['culture'] == culture]
        export_map_data[culture] = json.loads(sub_gdf.to_json())

    # --- 5. 保存文件 ---
    print(f"3. 保存文件... (AspectRatio: {global_aspect_ratio:.4f})")

    # 保存地图数据
    with open("split_map_data.json", "w", encoding='utf-8') as f:
        json.dump(export_map_data, f, ensure_ascii=False)

    # 保存默认配置 (注意：这会覆盖你的手动校准，请手动恢复)
    with open("layout_config.json", "w", encoding='utf-8') as f:
        json.dump(layout_config, f, indent=4)

    print("✅ 数据处理完成！")
    print("⚠️ 注意：layout_config.json 已被重置为计算值。")
    print("⚠️ 请立即使用手动校准的代码覆盖 layout_config.json 内容！")


if __name__ == "__main__":
    process_data()