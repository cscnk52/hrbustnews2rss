import requests
from bs4 import BeautifulSoup
from utils import fetch_total_pages
from datetime import datetime, timezone, timedelta
from feedgen.feed import FeedGenerator
from concurrent.futures import ThreadPoolExecutor
from config import column_dict, baseUrl


def fetch_detail_with_title(link_info):
    """
    爬取详情页内容和发布时间，并返回结果
    """
    title, url, is_external, pub_time = link_info
    if is_external:
        return title, url, is_external, "此条目为外部链接，点击原文查看", pub_time

    try:
        response = requests.get(url)
        response.encoding = "utf-8"
        if response.status_code != 200:
            return (
                title,
                url,
                is_external,
                f"详情页请求失败，状态码：{response.status_code}",
                None,
            )

        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", class_="v_news_content")
        description = content_div.decode_contents() if content_div else "详情内容未找到"

        info_paragraph = soup.find("p", class_="xinxi")
        if info_paragraph:
            date_span = info_paragraph.find(
                "span", string=lambda text: "日期时间：" in text if text else False
            )
            if date_span:
                date_text = date_span.get_text(strip=True).replace("日期时间：", "")
                pub_time = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")
                pub_time = pub_time.replace(tzinfo=timezone(timedelta(hours=8)))

        return title, url, is_external, description, pub_time

    except Exception as e:
        return title, url, is_external, f"爬取失败，错误信息：{e}", None


def fetch_and_generate_feed(column):
    """
    爬取指定栏目数据并直接生成 RSS Feed，包括分页逻辑，并标注外链，支持多线程
    """
    fg = FeedGenerator()
    fg.id(f"{baseUrl}{column}")
    fg.title(f"哈尔滨理工大学新闻网 - {column_dict.get(column, column)}")
    fg.author({"name": "HRBUST", "email": "info@hrbust.edu.cn"})
    fg.link(href=f"{baseUrl}{column}.htm", rel="alternate")
    fg.description(f"哈尔滨理工大学新闻网 - {column_dict.get(column, column)}")
    fg.language("zh")

    # 获取最后一页并解析总页数
    url = f"{baseUrl}{column}.htm"
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}，URL：{url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    total_pages = fetch_total_pages(soup)

    print(f"总页数为：{total_pages}")

    all_links = []

    # 爬取所有分页的文章链接，逆序构造请求
    for page in range(total_pages, 0, -1):
        if page == total_pages:
            page_url = f"{baseUrl}{column}.htm"  # 最后一页
        else:
            page_url = f"{baseUrl}{column}/{page}.htm"  # 其余页数

        response = requests.get(page_url)
        response.encoding = "utf-8"

        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}，URL：{page_url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        div_element = soup.find("div", class_="main-liebiao-con-left-bottom")

        if not div_element:
            print(f"第 {page} 页没有找到符合的内容")
            continue

        links = div_element.find_all("li", id=lambda x: x and x.startswith("line_u10"))
        if not links:
            print(f"第 {page} 页没有文章链接")
            continue

        for link in links:

            title = link.find("a").get_text(strip=True)
            href = link.find("a").get("href")

            # 判断是否为外部链接
            is_external = href.startswith("http")
            full_link = href if is_external else baseUrl + href

            # 提取并处理日期
            date_text = link.find("span").get_text(strip=True)
            pub_time = datetime.strptime(date_text, "%Y-%m-%d")
            pub_time = pub_time.replace(tzinfo=timezone(timedelta(hours=8)))

            all_links.append((title, full_link, is_external, pub_time))

        print(f"第 {page} 页爬取完成")

    # 多线程爬取详情页内容
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch_detail_with_title, all_links))

    # 排序结果按发布时间升序
    results = sorted(results, key=lambda x: x[4] or datetime.min)
    """
    此条目在“媒体理工”栏目下，链接配置出错，无法正确获取时间，若爬取该栏目，注释上方排序部分
    <li id="line_u10_8">
        <a
            href="哈尔滨理工大学“五个暖心礼”送别 2021 届硕博毕业生 - 东北网黑龙江 - 东北网  https://heilongjiang.dbw.cn/system/2021/04/09/058625123.shtml"
            target="_blank"
            title="东北网：哈尔滨理工大学“五个暖心礼”送别 2021 届硕博毕业生"
            >东北网：哈尔滨理工大学“五个暖心礼”送别 2021 届硕博毕业生</a
        >
        <span>2021-04-09</span>
    </li>
    """

    # 添加到 RSS Feed
    for title, full_link, is_external, description, pub_time in results:
        entry = fg.add_entry()
        entry.id(full_link)
        entry.title(title)
        entry.link(href=full_link)
        entry.description(description)
        if pub_time:
            entry.pubDate(pub_time)

    # 添加条目计数信息
    print(f"共 {len(results)} 条新闻")  # 条目数量统计

    return fg
