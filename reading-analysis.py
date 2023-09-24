import json
import re
import time
import urllib
from collections import defaultdict
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

global book_cache


def load_cache():
    try:
        with open('book_cache.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_cache():
    with open('book_cache.json', 'w', encoding='utf-8') as f:
        json.dump(book_cache, f, ensure_ascii=False, indent=4)


def book_search(book_title):
    # 检查缓存是否存在该书籍的链接
    if book_title in book_cache:
        return book_cache[book_title]
    # 创建浏览器对象
    browser = webdriver.PhantomJS(executable_path=".\webdriver\phantomjs.exe")  # Windows
    # 请求网址
    encoded_title = urllib.parse.quote(book_title)
    browser.get("https://book.douban.com/subject_search?search_text=" + encoded_title + "&cat=1001")
    # 解析网页信息
    soup = BeautifulSoup(browser.page_source, "lxml")
    # 读取标签内容
    tags = soup.select("#root > div > div > div > div > div > div > a")
    # 正则查找 href 链接
    link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(tags[0]))
    # 关闭浏览器
    browser.close()
    # 将链接存入缓存
    book_cache[book_title] = link_list[0]
    save_cache()
    return link_list[0]


def get_rating(soup):
    # 豆瓣评分及评价人数
    rating = soup.find('div', {'class': 'rating_self clearfix'})
    rating_num = rating.find('strong').string.strip()
    if not rating_num:
        rating_num = "-"
        rating_people = "评价人数不足"
    else:
        rating_people = rating.find('span', property="v:votes").string.strip()
    return rating_num, rating_people


def get_book_pages(book_info_soup):
    # 提取书籍的页数
    span_list = book_info_soup.findChild('div', {'id': 'info'})
    info_text = str(span_list.get_text())
    pages_match = re.search(r'页数:\s*(\d+)', info_text)
    if pages_match:
        return int(pages_match.group(1))
    else:
        return 1  # 默认为1页


def book_info(douban_link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    # 请求网址
    g = requests.get(douban_link, headers=headers)
    # 解析网页信息
    soup = BeautifulSoup(g.content, "lxml")
    return soup  # 返回 BeautifulSoup 解析对象


def analyze_reading_data(data):
    total_pages = 0
    total_duration = 0
    total_rating_count = 0
    total_rating_sum = 0
    valid_books_count = 0
    start_time = time.time()  # 记录开始时间
    borrow_dates = defaultdict(int)  # 用于统计借书日期
    return_dates = defaultdict(int)  # 用于统计还书日期

    for idx, item in enumerate(data, 1):
        douban_link = book_search(item["name"])
        book_info_soup = book_info(douban_link)
        rating_num, rating_people = get_rating(book_info_soup)

        if rating_num != "-" and float(rating_num) > 0:
            valid_books_count += 1
            total_rating_count += int(rating_people.replace("人评价", ""))
            total_rating_sum += float(rating_num)

        pages = get_book_pages(book_info_soup)
        total_pages += pages
        item['pages'] = pages

        total_duration += item["dura"]

        # 处理日期部分，统计借书和还书日期
        borrow_date, return_date = process_dates(item)
        borrow_dates[borrow_date.strftime("%Y-%m")] += 1
        return_dates[return_date.strftime("%Y-%m")] += 1

        print(f"处理书籍 {idx}/{len(data)} 完成")
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time
        print(f"总运行时间: {elapsed_time:.2f} 秒")
    average_pages_per_day = total_pages / total_duration if total_duration > 0 else 0

    if valid_books_count > 0:
        average_rating_count = total_rating_count / valid_books_count
        average_rating = total_rating_sum / valid_books_count
    else:
        average_rating_count = 0
        average_rating = 0

    return average_pages_per_day, average_rating_count, average_rating, borrow_dates, return_dates


def most_read_type(data):
    type_count = {}  # 用于统计每种类型的阅读数

    for item in data:
        book_type = item["type"]
        if book_type in type_count:
            type_count[book_type] += 1
        else:
            type_count[book_type] = 1

    # 找到阅读数最多的类型
    most_read_type = max(type_count, key=type_count.get)
    most_read_count = type_count[most_read_type]

    return most_read_type, most_read_count


def process_dates(item):
    borrow_date = datetime.strptime(item["borrow"], "%Y-%m-%d")
    return_date = datetime.strptime(item["return"], "%Y-%m-%d")
    return borrow_date, return_date


def main():
    global book_cache
    book_cache = load_cache()
    data = [
        {
            "name": "寓言中的经济学:插图精装版",
            "borrow": "2022-03-28",
            "return": "2022-04-07",
            "type": "经济",
            "dura": 10
        },
        {
            "name": "第一次炒股票买基金就赚钱",
            "borrow": "2022-03-16",
            "return": "2022-03-17",
            "type": "经济",
            "dura": 1
        },
        {
            "name": "你一定要知道的经济常识全集",
            "borrow": "2021-12-09",
            "return": "2021-12-20",
            "type": "经济",
            "dura": 11
        },
        {
            "name": "Python编程入门",
            "borrow": "2023-01-15",
            "return": "2023-01-25",
            "type": "编程",
            "dura": 10
        },
        {
            "name": "半小时漫画经济学·生活常识篇",
            "borrow": "2021-11-30",
            "return": "2021-12-09",
            "type": "经济",
            "dura": 9
        },
    ]

    average_pages_per_day, average_rating_count, average_rating, borrow_dates, return_dates = analyze_reading_data(data)
    most_read_type_data, most_read_count = most_read_type(data)

    print(f"平均每天阅读页数: {average_pages_per_day:.2f} 页")
    print(f"阅读的书籍的平均评价人数: {average_rating_count:.2f} 人")
    print(f"阅读的书籍的平均评分: {average_rating:.2f}")
    print(f"阅读数最多的类型是: {most_read_type_data}，共有 {most_read_count} 本书")

    # 统计借书量最高的时间段
    max_borrow_month = max(borrow_dates, key=borrow_dates.get)
    max_borrow_count = borrow_dates[max_borrow_month]
    print(f"借书量最高的时间段是: {max_borrow_month}，共借阅 {max_borrow_count} 本书")

    # 统计还书量最高的时间段
    max_return_month = max(return_dates, key=return_dates.get)
    max_return_count = return_dates[max_return_month]
    print(f"还书量最高的时间段是: {max_return_month}，共还书 {max_return_count} 本书")


if __name__ == "__main__":
    main()
