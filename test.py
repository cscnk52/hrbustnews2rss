import unittest
import feedparser


class TestFeedParser(unittest.TestCase):

    def setUp(self):
        # 设置测试所需的环境或变量
        self.column = "jxky"  # 示例栏目
        self.test_feed_file = "rss_feed.xml"  # 文件名

    def test_rss_feed_parsing(self):
        # 分类记录错误信息
        missing_title_entries = []
        missing_link_entries = []
        missing_published_entries = []
        missing_description_entries = []

        try:
            # 使用 feedparser 解析 RSS Feed
            feed = feedparser.parse(self.test_feed_file)

            # 验证解析后的 RSS Feed 的各个属性
            self.assertIsNotNone(feed.entries, "RSS Feed entries 不应为 None")
            self.assertGreater(len(feed.entries), 0, "RSS Feed entries 的数量应大于 0")

            # 验证每个条目的信息
            for entry in feed.entries:
                link = getattr(entry, "link", "未知链接")

                if not hasattr(entry, "title") or entry.title is None:
                    missing_title_entries.append(link)

                if not hasattr(entry, "link") or entry.link is None:
                    missing_link_entries.append(link)

                if not hasattr(entry, "published") or entry.published is None:
                    missing_published_entries.append(link)

                if not hasattr(entry, "description") or entry.description is None:
                    missing_description_entries.append(link)

            # 打印分类错误信息
            if missing_title_entries:
                print("缺少标题的条目：")
                for link in missing_title_entries:
                    print(f" - {link}")

            if missing_link_entries:
                print("缺少链接的条目：")
                for link in missing_link_entries:
                    print(f" - {link}")

            if missing_published_entries:
                print("缺少发布日期的条目：")
                for link in missing_published_entries:
                    print(f" - {link}")

            if missing_description_entries:
                print("缺少描述字段的条目：")
                for link in missing_description_entries:
                    print(f" - {link}")

        except Exception as e:
            self.fail(f"feedparser 解析失败，错误信息：{e}")


if __name__ == "__main__":
    unittest.main()
