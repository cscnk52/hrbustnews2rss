import re


def fetch_total_pages(soup):
    """
    从分页信息中提取总页数
    """
    pagination_td = soup.find("td", id="fanye137504")
    if pagination_td:
        match = re.search(r"\d+/(\d+)", pagination_td.get_text(strip=True))
        if match:
            return int(match.group(1))  # 返回总页数
    return 1  # 默认返回 1，表示仅有一页
