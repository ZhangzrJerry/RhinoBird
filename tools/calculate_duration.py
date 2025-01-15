from datetime import datetime, timedelta

# 创建一个空集合来记录借书的日期
borrowed_dates = set()

# 遍历数据，将借书的日期添加到集合中
def calculate_duration(data):
    for item in data:
        borrow_date = datetime.strptime(item["borrow"], "%Y-%m-%d")
        return_date = datetime.strptime(item["return"], "%Y-%m-%d")
        current_date = borrow_date
        while current_date <= return_date:
            borrowed_dates.add(current_date.strftime("%Y-%m-%d"))
            current_date = current_date + timedelta(days=1)

    # 统计不同的借书日期数量
    unique_borrowed_days = len(borrowed_dates)
    return unique_borrowed_days