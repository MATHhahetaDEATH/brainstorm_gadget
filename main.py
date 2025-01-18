import webbrowser
import time
import os
import requests
import matplotlib.pyplot as plt
from urllib.parse import quote
from modules.word_count import word_count
from modules.word_cloud import generate_wordcloud


def open_search_page(keyword):
    # 替换URL中的"自我"为用户输入的关键词
    base_url = "http://ccl.pku.edu.cn:8080/ccl_corpus/search?q={}+path%3ACWAC&q1={}&LastQuery={}&start=0&num=50&index=FullIndex&outputFormat=HTML&encoding=UTF-8&isForReading=no&patternNature=&dir=xiandai&startTime=&endTime=&xiandaiStartTime=&xiandaiEndTime=&maxLeftLength=30&maxRightLength=30&neighborSortLength=0&orderStyle=score&scopestr=&search=查询"
    search_url = base_url.format(quote(keyword), quote(keyword), quote(keyword), quote(keyword))
    
    # 使用浏览器打开搜索页面
    print(f"正在打开搜索页面，请稍等...")
    webbrowser.open(search_url)
    
    print(f"请下载该页面提供的txt文件并放入本程序根目录。下载完成后，请按Enter键继续...")
    input("按Enter键继续...")

def filter_nouns(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 假设文件中的每一行是一个词及其频次，用空格分隔
    word_freq = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            word_freq.append((parts[0], int(parts[1])))
    
    # 过滤出频数大于或等于 10 的项
    word_freq_filtered = [item for item in word_freq if item[1] >= 10]
    
    # 生成输出的内容
    output_lines = ["这是一份词频统计表，第一列是词语，第二列是频数，请筛选出其中的形容词、名词、动词项并保持整个列表格式不变，即仍然为第一列词语、第二列频数的纯文本非markdown格式\n"]
    for word, freq in word_freq_filtered:
        output_lines.append(f"{word}\t{freq}\n")
    
    # 将结果保存到 prompt.txt 文件
    with open('prompt.txt', 'w', encoding='utf-8') as output_file:
        output_file.writelines(output_lines)

    # 引导用户利用ai筛选名词
    print(f"请将该目录下的prompt.txt文件投喂给任意一个对话式ai并将其回复覆盖prompt.txt（接下来您也可以手动剔除一些不想要的项）。操作完成后，请按Enter键继续...")
    input("按Enter键继续...")
    word_freq = open('prompt.txt', 'r', encoding='utf-8')

    return word_freq

def read_word_freq(file):
    word_freq = {}
    for line in file:
        parts = line.split()
        if len(parts) == 2:
            word_freq[parts[0]] = int(parts[1])
    return word_freq

def main():
    # 获取用户输入的关键词
    keyword = input("请输入查询的关键词：")
    
    # 步骤1: 打开查询页面，指导用户下载txt文件
    open_search_page(keyword)
    
    # 步骤2: 用户下载的txt文件路径
    input_txt_path = f"corpus_{keyword}_path_CWAC.txt"
    
    # 步骤3: 将txt文件导入word_count.py进行词频统计
    output_txt_path = "word_count_output.txt"
    word_count(input_txt_path, output_txt_path)
    
    # 步骤4: 引导用户利用ai筛选出现次数大于10的实词
    filtered_word_freq = read_word_freq(filter_nouns(output_txt_path))

    # 步骤5: 生成词云
    output_image_path = "wordcloud_output.png"
    font_path = "SourceHanSerifSC-SemiBold.otf"  # 替换为你系统中中文字体文件的路径
    while True:
        generate_wordcloud(filtered_word_freq, output_image_path, font_path)
        
        # 显示并询问用户是否满意
        img = plt.imread(output_image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        
        user_input = input("您喜欢这个词云吗？(y/n): ")
        if user_input.lower() == 'y':
            print("词云生成完毕！")
            break
        else:
            print("正在重新生成词云...")

if __name__ == '__main__':
    main()
