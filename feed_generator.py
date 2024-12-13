def save_rss_feed(fg, filename):
    fg.rss_file(filename)  # 输出到文件
    print(f"RSS Feed 生成完成，保存为 {filename}")
