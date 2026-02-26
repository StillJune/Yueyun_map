from pyecharts import options as opts
from pyecharts.charts import Map
import json

def create_map():
    with open("guangdong_culture.json", "r", encoding="utf-8") as f:
        gd_data = json.load(f)

    data_pair = []
    for feat in gd_data['features']:
        name = feat['properties']['name']
        culture = feat['properties'].get('culture', '其他')
        # 为不同文化分配数值用于视觉映射
        val = 1 if culture == "广府文化" else (2 if culture == "潮汕文化" else 3)
        data_pair.append((name, val))

    c = (
        Map(init_opts=opts.InitOpts(width="100%", height="100vh", bg_color="transparent"))
        .add(
            series_name="广东文化地图",
            data_pair=data_pair,
            maptype="广东", # 这里名字要和前端 registerMap 一致
            layout_center=["50%", "50%"],  # 强制地图中心对齐容器中心
            layout_size="100%",  # 强制地图大小占满容器
            is_roam=False,
            label_opts=opts.LabelOpts(is_show=True, color="#333"),
            itemstyle_opts=opts.ItemStyleOpts(
                border_color="#555", border_width=1
            ),
            emphasis_itemstyle_opts=opts.ItemStyleOpts(
                area_color="rgba(255, 215, 0, 0.8)", border_width=2
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="粤韵千里图", pos_left="center", title_textstyle_opts=opts.TextStyleOpts(font_size=24)),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"value": 1, "label": "广府文化", "color": "rgba(200, 80, 50, 0.7)"},
                    {"value": 2, "label": "潮汕文化", "color": "rgba(50, 100, 150, 0.7)"},
                    {"value": 3, "label": "客家文化", "color": "rgba(80, 150, 80, 0.7)"}
                ],
                pos_left="5%", pos_bottom="5%"
            )
        )
    )
    return c


if __name__ == "__main__":
    map_chart = create_map()
    map_chart.render("templates/map_component.html")
    print("地图已生成: templates/map_component.html")