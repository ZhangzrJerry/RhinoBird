import json
import re
import time
import urllib
from collections import defaultdict
from datetime import datetime
import jieba
from collections import Counter
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


# def get_rating(soup):
#     # 豆瓣评分及评价人数
#     rating = soup.find('div', {'class': 'rating_self clearfix'})
#     rating_num = rating.find('strong').string.strip()
#     if not rating_num:
#         rating_num = "-"
#         rating_people = "评价人数不足"
#     else:
#         rating_people = rating.find('span', property="v:votes").string.strip()
#     return rating_num, rating_people


def get_book_info(book_info_soup):
    author_match_grouped = ''
    # 提取评分与评价人数
    rating = book_info_soup.find('div', {'class': 'rating_self clearfix'})
    rating_num = rating.find('strong').string.strip()
    if not rating_num:
        rating_num = "-"
        rating_people = "评价人数不足"
    else:
        rating_people = rating.find('span', property="v:votes").string.strip()
    # 提取书籍的页数和出版年
    span_list = book_info_soup.findChild('div', {'id': 'info'})
    info_text = str(span_list.get_text())
    pages_match = re.search(r'页数:\s*(\d+)', info_text)
    author_match = re.search(r'作者:\s*(.+)', info_text)
    if author_match.group(1).endswith(" 著"):
        author_match_grouped = author_match.group(1)[:-2]
    else:
        author_match_grouped = author_match.group(1)
    author_match_grouped = author_match_grouped.replace(" ", "")
    if pages_match:
        pages = int(pages_match.group(1))
    else:
        pages = 1  # 默认为1页
    print(author_match_grouped)
    return pages, rating_num, rating_people, author_match_grouped


def book_info(douban_link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    # 请求网址
    g = requests.get(douban_link, headers=headers)
    # 解析网页信息
    soup = BeautifulSoup(g.content, "lxml")
    return soup  # 返回 BeautifulSoup 解析对象


def analyze_reading_data(data):
    stop_words = [
        "的", "是", "在", "之", "与", "和", "了", "不", "中", "要", "这", "那", "如何", "为什么", "怎么", "什么",
        "哪些",
        "哪个", "哪里", "哪儿",
        "有", "没有", "可以", "不可以", "能", "不能", "我", "你", "他", "她", "它", "就", "都", "也", "而", "及", "与",
        "或", "但", "然而", "虽然", "因为",
        "所以", "因此", "但是", "从", "到", "上", "下", "前", "后", "里", "外", "边", "这个", "那个", "这些", "那些",
        "这里", "那里", "这儿", "那儿",
        "吧", "呢", "吗", "啊", "嗯", "哦", "嘛", "嘻嘻", "哈哈", "呵呵", "了解", "知道", "明白", "理解", "看", "读",
        "学",
        "研究", "书", "小", "大", "好", "坏", "多", "少", "高",
        "低", "长", "短", "新", "旧", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "万",
        "年",
        "月", "日", "时",
        "分", "秒", "上午", "下午", "晚上", "早上", "中午", "全集", "精装版", "一定", "定义", "重新"
    ]
    total_pages = 0
    total_duration = 0
    total_rating_count = 0
    author_counts = {}  # 统计作者出现次数
    total_rating_sum = 0
    valid_books_count = 0
    start_time = time.time()  # 记录开始时间
    borrow_dates = defaultdict(int)  # 用于统计借书日期
    return_dates = defaultdict(int)  # 用于统计还书日期
    total_borrow_count = 0
    word_counts = Counter()  # 使用jieba分词并统计词频
    longest_reading_time = 0
    longest_reading_book = ""

    for idx, item in enumerate(data, 1):
        keywords = jieba.cut(item["name"])
        word_counts.update(keywords)
        douban_link = book_search(item["name"])
        book_info_soup = book_info(douban_link)
        # rating_num, rating_people = get_rating(book_info_soup)
        pages, rating_num, rating_people, author_match_grouped = get_book_info(book_info_soup)
        # 提取书籍的作者信息
        if author_match_grouped in author_counts:
            author_counts[author_match_grouped] += 1
        else:
            author_counts[author_match_grouped] = 1

        if rating_num != "-" and float(rating_num) > 0:
            valid_books_count += 1
            total_rating_count += int(rating_people.replace("人评价", ""))
            total_rating_sum += float(rating_num)

        total_pages += pages
        item['pages'] = pages

        total_duration += item["dura"]

        # 更新阅读时间最长的书籍记录
        if item["dura"] > longest_reading_time:
            longest_reading_time = item["dura"]
            longest_reading_book = item["name"]

        # 处理日期部分，统计借书和还书日期
        borrow_date, return_date = process_dates(item)
        borrow_dates[borrow_date.strftime("%Y-%m")] += 1
        return_dates[return_date.strftime("%Y-%m")] += 1
        total_borrow_count += 1
        print(f"处理书籍 {idx}/{len(data)} 完成")
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time
        print(f"总运行时间: {elapsed_time:.2f} 秒")
    # most_read_author, most_read_count = author_counts.most_common(1)[0] if author_counts else ("N/A", 0)
    average_pages_per_day = total_pages / total_duration if total_duration > 0 else 0
    filtered_word_counts = {word: count for word, count in word_counts.items() if
                            word not in stop_words and len(word) > 1 and count > 1}
    top_three_words = Counter(filtered_word_counts).most_common(3)
    # for word, count in filtered_word_counts.items():
    #     print(f"词汇'{word}'出现次数: {count}")
    type_counts = Counter([book["type"] for book in data])
    most_common_types = type_counts.most_common(2)
    characteristics_set = set([word for word, count in top_three_words] + [type for type, count in most_common_types])
    characteristics = list(characteristics_set)
    if valid_books_count > 0:
        average_rating_count = total_rating_count / valid_books_count
        average_rating = total_rating_sum / valid_books_count
    else:
        average_rating_count = 0
        average_rating = 0

    return average_pages_per_day, average_rating_count, average_rating, borrow_dates, return_dates, total_borrow_count, \
           longest_reading_book, longest_reading_time, characteristics, author_counts


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


def count_borrow_and_return_by_month(data):
    borrow_counts = defaultdict(int)
    return_counts = defaultdict(int)

    for item in data:
        borrow_date, return_date = process_dates(item)
        borrow_month = borrow_date.strftime("%Y-%m")
        return_month = return_date.strftime("%Y-%m")

        borrow_counts[borrow_month] += 1
        return_counts[return_month] += 1

    return borrow_counts, return_counts


def main():
    global book_cache
    book_cache = load_cache()
    data = [
        {
            "name": "洗澡",
            "borrow": "2023-02-25",
            "return": "2023-03-20",
            "type": "文学",
            "dura": 23
        },
        {
            "name": "加缪的手记·第一卷：1935.5-1942.2",
            "borrow": "2023-02-06",
            "return": "2023-02-13",
            "type": "哲学、宗教",
            "dura": 7
        },
        {
            "name": "第一人称单数",
            "borrow": "2023-04-19",
            "return": "2023-05-05",
            "type": "文学",
            "dura": 16
        },
        {
            "name": "被抹去的历史:巴拿马运河无人诉说的故事",
            "borrow": "2023-04-05",
            "return": "2023-04-10",
            "type": "历史、地理",
            "dura": 5
        },
        {
            "name": "马可瓦尔多",
            "borrow": "2023-03-27",
            "return": "2023-04-10",
            "type": "文学",
            "dura": 14
        },
        {
            "name": "大脑喜欢听你这样说",
            "borrow": "2023-05-08",
            "return": "2023-05-15",
            "type": "哲学、宗教",
            "dura": 7
        },
        {
            "name": "霍乱时期的爱情",
            "borrow": "2023-05-24",
            "return": "2023-06-02",
            "type": "文学",
            "dura": 9
        },
        {
            "name": "雪山飞狐",
            "borrow": "2022-11-07",
            "return": "2022-11-09",
            "type": "文学",
            "dura": 2
        },
        {
            "name": "新诗十讲",
            "borrow": "2021-09-13",
            "return": "2021-09-26",
            "type": "文学",
            "dura": 13
        },
        {
            "name": "闻一多画传",
            "borrow": "2021-09-13",
            "return": "2021-09-13",
            "type": "历史、地理",
            "dura": 0
        },
        {
            "name": "有趣儿:老舍笔下的人生幽默",
            "borrow": "2023-07-04",
            "return": "2023-07-06",
            "type": "文学",
            "dura": 2
        },
        {
            "name": "活着",
            "borrow": "2023-02-06",
            "return": "2023-02-06",
            "type": "文学",
            "dura": 0
        },
        {
            "name": "苏北少年“堂吉诃德”",
            "borrow": "2023-02-13",
            "return": "2023-03-20",
            "type": "文学",
            "dura": 35
        },
        {
            "name": "中国妖怪",
            "borrow": "2023-04-05",
            "return": "2023-04-10",
            "type": "文学",
            "dura": 5
        },
        {
            "name": "长河",
            "borrow": "2023-04-10",
            "return": "2023-04-19",
            "type": "文学",
            "dura": 9
        },
        {
            "name": "强风吹拂",
            "borrow": "2023-05-18",
            "return": "2023-05-24",
            "type": "文学",
            "dura": 6
        },
        {
            "name": "你的行为使我们恐惧",
            "borrow": "2023-05-15",
            "return": "2023-05-18",
            "type": "文学",
            "dura": 3
        },
        {
            "name": "红楼夜话",
            "borrow": "2023-06-02",
            "return": "2023-06-19",
            "type": "文学",
            "dura": 17
        },
        {
            "name": "再袭面包店",
            "borrow": "2023-06-19",
            "return": "2023-06-21",
            "type": "文学",
            "dura": 2
        },
        {
            "name": "名侦探的守则",
            "borrow": "2022-10-09",
            "return": "2022-11-09",
            "type": "文学",
            "dura": 31
        }
    ]

    average_pages_per_day, average_rating_count, average_rating, borrow_dates, return_dates, total_borrow_count, \
    longest_reading_book, longest_reading_time, characteristics, author_counts = analyze_reading_data(data)
    most_read_type_data, most_read_count = most_read_type(data)
    print(f"平均每天阅读页数: {average_pages_per_day:.2f} 页")
    print(f"阅读的书籍的平均评价人数: {average_rating_count:.2f} 人")
    print(f"阅读的书籍的平均评分: {average_rating:.2f}")
    print(f"阅读数最多的类型是: {most_read_type_data}，共有 {most_read_count} 本书")
    print(f"总借书数量: {total_borrow_count}")
    print(f"阅读关键词包括：{characteristics}")
    # 统计借书量最高的时间段
    max_borrow_month = max(borrow_dates, key=borrow_dates.get)
    max_borrow_count = borrow_dates[max_borrow_month]
    print(f"借书量最高的时间段是: {max_borrow_month}，共借阅 {max_borrow_count} 本书")

    # 统计还书量最高的时间段
    max_return_month = max(return_dates, key=return_dates.get)
    max_return_count = return_dates[max_return_month]
    print(f"还书量最高的时间段是: {max_return_month}，共还书 {max_return_count} 本书")

    borrow_counts, return_counts = count_borrow_and_return_by_month(data)

    # 统计借还书细则
    all_months = set(borrow_counts.keys()) | set(return_counts.keys())
    for month in sorted(all_months):
        borrow_count = borrow_counts[month]
        return_count = return_counts[month]
        print(f"{month}；借书数量{borrow_count}本，还书数量{return_count}本")

    if longest_reading_time > 0:
        print(f"阅读时间最长的书籍是：{longest_reading_book}，共阅读了 {longest_reading_time} 天")
    else:
        print("没有阅读记录")
    most_common_author = max(author_counts, key=author_counts.get) if author_counts else "N/A"
    most_common_author_count = author_counts.get(most_common_author, 0)
    print(f"阅读书籍中最多的作者是：{most_common_author}，共出现了 {most_common_author_count} 次")


if __name__ == "__main__":
    main()
