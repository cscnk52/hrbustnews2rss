import re
import sqlite3
import feedparser

# 初始化数据库连接
conn = sqlite3.connect("rss_feed.db")
cursor = conn.cursor()

# 创建表格（如果不存在）
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS rss_feed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        column TEXT,
        title TEXT,
        link TEXT,
        published TEXT,
        summary TEXT
    )
    """
)

# 解析 RSS 文件
rss_file = "rss_feed.xml"
feed = feedparser.parse(rss_file)
column_match = re.search(r"哈尔滨理工大学新闻网\s-\s(.+)", feed.feed.get("title", ""))
column = column_match.group(1) if column_match else "未知栏目"

# 将数据存入数据库
for entry in feed.entries:
    title = entry.get("title", "No Title")
    link = entry.get("link", "No Link")
    published = entry.get("published", "No Date")
    summary = entry.get("summary", "No Summary")

    cursor.execute(
        """
        INSERT INTO rss_feed (column, title, link, published, summary)
        VALUES (?, ?, ?, ?, ?)
        """,
        (column, title, link, published, summary),
    )

# 提交事务并关闭数据库连接
conn.commit()
conn.close()

print("RSS 数据已成功存入数据库！")
