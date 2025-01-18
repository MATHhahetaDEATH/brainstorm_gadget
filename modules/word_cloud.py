import argparse
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 创建词云
def generate_wordcloud(word_freq, output_path, font_path):
    # 创建词云对象，并指定字体路径
    wordcloud = WordCloud(
        width=3000,  # 词云图的宽度
        height=2000,  # 词云图的高度
        background_color='white',  # 背景颜色
        colormap='cividis',  # 词云的配色方案
        max_words=200,  # 显示的最大词数
        font_path=font_path,  # 指定中文字体路径
        relative_scaling=0.5,  # 控制词语大小与位置的相对缩放，值越大间距越大
        prefer_horizontal=0.7,  # 词语横向排列的比例（0~1）
        max_font_size=600,  # 最大字体大小
        min_font_size=80,  # 最小字体大小
        font_step=3,  # 字体步进（即字体大小变化的步伐）
    ).generate_from_frequencies(word_freq)

    # 保存词云到指定路径
    wordcloud.to_file(output_path)
    print(f"词云已保存到: {output_path}")

# 主函数
def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="生成词云")
    parser.add_argument('input_file', type=str, help="输入文件路径")
    parser.add_argument('output_file', type=str, help="输出图片文件路径")
    parser.add_argument('font_path', type=str, help="字体文件路径（如思源宋体）")

    # 解析命令行参数
    args = parser.parse_args()

    # 读取词频数据
    word_freq = read_word_freq(args.input_file)

    # 生成并保存词云
    generate_wordcloud(word_freq, args.output_file, args.font_path)

if __name__ == '__main__':
    main()
