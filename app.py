from flask import Flask, render_template
import json
import os

app = Flask(__name__)

# === 城市数据 (示例) ===
CITY_DATA = {
    "广州市": {"desc": "广府文化核心地，千年商都，美食之都。"},
    "佛山市": {"desc": "武术之乡，陶艺之都，广府文化发源地之一。"},
    "湛江市": {"desc": "中国海鲜美食之都，港城风光旖旎。"},
    "茂名市": {"desc": "南方油城，荔枝之乡，年例文化独特。"},
    "潮州市": {"desc": "国家历史文化名城，工夫茶、潮绣、木雕闻名。"},
    "汕头市": {"desc": "百载商埠，经济特区，美食孤岛。"},
    "梅州市": {"desc": "世界客都，叶帅故里，围龙屋错落有致。"},
    # ... 可继续添加其他城市
}


@app.route('/')
def index():
    # 1. 读取布局配置 (校准后的坐标)
    with open("layout_config.json", "r", encoding="utf-8") as f:
        layout_config = json.load(f)

    # 2. 读取地图数据 (由 Step 1 生成)
    with open("split_map_data.json", "r", encoding="utf-8") as f:
        map_data = json.load(f)

    return render_template('index.html',
                           layout_config=json.dumps(layout_config),
                           map_data=json.dumps(map_data),
                           city_data=json.dumps(CITY_DATA, ensure_ascii=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)