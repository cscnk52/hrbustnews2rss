---
theme: academic
layout: cover
coverAuthor: cscnk52
coverAuthorUrl: https://github.com/cscnk52
coverDate: 2024/12/13
transition: fade
---

# 基于 Python 的 RSSHub 实现

---
layout: figure-side
figureUrl: ./images/Feed-icon.svg
---

# 何为 RSS

**RSS**<sup>1</sup>（英文全称：RDF Site Summary 或 Really Simple Syndication），中文译作简易信息聚合，也称聚合内容，是一种消息来源格式规范，用以聚合多个网站更新的内容并自动通知网站订阅者。

使用 RSS 后，网站订阅者便无需再手动查看网站是否有新的内容，同时 RSS 可将多个网站更新的内容进行整合，以摘要的形式呈现，有助于订阅者快速获取重要信息，并选择性地点阅查看。

<Footnotes separator>
  <Footnote :number=1><a href="https://zh.wikipedia.org/wiki/RSS" rel="noreferrer" target="_blank">RSS - 维基百科</a></Footnote>
</Footnotes>

---
layout: figure-side
figureUrl: ./images/rsshub-logo.png
---

# 何为 RSSHub

**RSSHub**<sup>1</sup> 是一个开源、简单易用、易于扩展的 RSS 生成器，可以给任何奇奇怪怪的内容生成 RSS 订阅源。RSSHub 借助于开源社区的力量快速发展中，目前已适配数百家网站的上千项内容。

<Footnotes separator>
  <Footnote :number=1><a href="https://github.com/DIYgod/RSSHub" rel="noreferrer" target="_blank">RSSHub - GitHub</a></Footnote>
</Footnotes>

---

# 代码构成

```
.
├── config.py			# 存储配置
├── database.py			# 数据库操作相关
├── feed_generator.py	# 生成 RSS 文件
├── fetch.py			# 抓取网页内容
├── main.py				# 入口文件
├── test.py				# 测试文件
└── utils.py			# 实用函数
```

以抓取[哈理工新闻网](https://news.hrbust.edu.cn/lgyw.htm)下`理工要闻` 栏目为例，抓取所有新闻条目，然后输出成规范的 RSS 文件，并存入 SQLite 数据库中。

---

# RSS 文件频道规范<sup>1</sup>

| **Element**     | **Description**                                                                                                                                                                                                             | **Example**                                                                |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **title**       | The name of the channel. It's how people refer to your service. If you have an HTML website that contains the same information as your RSS file, the title of your channel should be the same as the title of your website. | GoUpstate.com News Headlines                                               |
| **link**        | The URL to the HTML website corresponding to the channel.                                                                                                                                                                   | http://www.goupstate.com/                                                  |
| **description** | Phrase or sentence describing the channel.                                                                                                                                                                                  | The latest news from GoUpstate.com, a Spartanburg Herald-Journal Web site. |

<Footnotes separator>
  <Footnote :number=1><a href="https://www.rssboard.org/rss-specification#requiredChannelElements" rel="noreferrer" target="_blank">RSS 2.0 Specification - Required channel elements</a></Footnote>
</Footnotes>

---

# RSS 文件条目规范<sup>1</sup>

| **Element**     | **Description**                                                                                                                        | **Example**                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **title**       | The title of the item.                                                                                                                 | Venice Film Festival Tries to Quit Sinking                                                   |
| **link**        | The URL of the item.                                                                                                                   | http://nytimes.com/2004/12/07FEST.html                                                       |
| **description** | The item synopsis.                                                                                                                     | &lt;description&gt;Some of the most heated chatter at the Venice Film...&lt;/description&gt; |
| **guid**        | A string that uniquely identifies the item. <a href="https://www.rssboard.org/rss-specification#ltguidgtSubelementOfLtitemgt">More</a> |                                                                                              |
| **pubDate**     | Indicates when the item was published. <a href="https://datatracker.ietf.org/doc/html/rfc822#section-5">More.</a>                      |                                                                                              |

<Footnotes separator>
  <Footnote :number=1><a href="https://www.rssboard.org/rss-specification#hrelementsOfLtitemgt" rel="noreferrer" target="_blank">RSS 2.0 Specification - Elements of &lt;item&gt;</a></Footnote>
</Footnotes>

---

# 使用到的第三方库

- black - 用于格式化 Python 代码
- bs4<sup>1</sup> - 用于解析爬取的 HTML 数据
- concurrent - 用于多线程爬取数据
- datetime - 用于处理时间
- feedgen - 生成规范的 RSS 文件
- feedparser - 解析 RSS 文件
- re - 正则表达式用于提取字符串
- sqlite3 - 用于 SQLite 数据库操作
- unittest - 用于单元测试
  命令行

<Footnotes separator>
  <Footnote :number=1>Dummy package for Beautiful Soup (beautifulsoup4)</Footnote>
</Footnotes>

---

# Reference:

- DIYgod. (2024, June 19). The crash and rebirth of a six-year-old open source project. https://diygod.cc/6-year-of-rsshub
- DIYgod. (n.d.). DIYgod/rsshub: 🧡 everything is RSSible. GitHub. https://github.com/DIYgod/RSSHub
- RSS Advisory Board. RSS icon. (n.d.). https://www.rssboard.org/rss-specification
- Wikimedia Foundation. (2024, December 12). RSS. Wikipedia. https://zh.wikipedia.org/wiki/RSS

<Footnotes separator>
  <Footnote>Slide generated by <a href="https://sli.dev/"> slidev </a></Footnote>
</Footnotes>
