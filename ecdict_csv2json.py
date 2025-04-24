import pandas as pd
import json
from tqdm import tqdm

csv_file_path = 'ecdict.csv'
json_file_path = 'ecdict.json'

try:
    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path)

    # 提取第一列和第三列
    key_column = df.iloc[:, 0]
    value_column = df.iloc[:, 3]

    # 构建字典
    result_dict = dict(zip(key_column, value_column))

    filtered_dict = {}
    for key, value in tqdm(result_dict.items()):
        key = str(key)
        # 检查键名是否包含英文字母
        if any(s.isalpha() for s in key):
            # 检查值是否不为 nan 且不全是英文
            if pd.notna(value) and not all(s.isalpha() for s in value):
                filtered_dict[key] = value
    # 保存为 JSON 文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_dict, f, ensure_ascii=False)

    print(f"数据已成功保存到 {json_file_path}。")

except FileNotFoundError:
    print(f"错误: 文件 {csv_file_path} 未找到。")
except Exception as e:
    print(f"错误: 发生未知错误: {e}")
    