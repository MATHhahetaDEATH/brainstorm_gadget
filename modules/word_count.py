#coding=utf-8
import jieba
import re
import argparse
from collections import Counter

def word_count(input_path, output_path): 
    try: 
        # 导入要处理的文本
        with open(input_path, "r", encoding="gb18030") as f:
            txt = f.read()

        # 使用正则表达式移除【】括号及其中的内容
        txt = re.sub(r'\u3010.*?\u3011', '', txt)

        # 加入要去除的标点符号
        excludes = {"，", "。", "\n", "-", "“", "”", "：", "；", "？", "（", "）", "！", "…", "..."}

        # 利用jieba分词
        words = jieba.lcut(txt)

        # 只保留长度大于等于2的词语
        words = [word for word in words if len(word) >= 2 and not re.search(r'\d', word)]

        # 设置初始计数数组
        counts = Counter(words)

        # 去除标点符号
        for word in excludes:
            counts.pop(word, None)

        # 根据词出现次数进行排序
        items = counts.most_common()

        # 将数据写入输出文件
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for word, count in items:
                output_file.write(f"{word}   {count}\n")
                # print(f"{word:<10}{count:>5}")

    except FileNotFoundError:
        print("文件未找到，请检查路径是否正确。")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    # 设置参数解析器
    parser = argparse.ArgumentParser(description="词频统计。")
    parser.add_argument('input_file', help="输入文件的路径")
    parser.add_argument('output_file', help="输出文件的路径")

    # 解析参数
    args = parser.parse_args()

    # 调用函数处理文件
    word_count(args.input_file, args.output_file)
