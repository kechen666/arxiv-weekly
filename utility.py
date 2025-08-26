from datetime import datetime, timedelta, timezone

def get_new_papers_date():
    """
    获取当前最新论文的时间区间（基于 arXiv 更新策略）。
    - 若当前时间在 UTC 1:00 之前，则认为使用前一天作为目标日期
    - 每个工作日对应不同的时间偏移区间（UTC 19:00 到次日 19:00）
    :return: (start_time, end_time) datetime 对象
    """
    current_time = datetime.now(timezone.utc)

    # 如果当前时间在 1:00 之前，使用前一天
    target_date = current_time - timedelta(days=1) if current_time.hour < 1 else current_time

    # 获取目标日期的星期几 (0=Monday, 6=Sunday)
    weekday = target_date.weekday()

    # delta_list: 每个工作日对应的起止偏移
    delta_list = [
        [-4, -3],  # Monday
        [-4, -1],  # Tuesday
        [-2, -1],  # Wednesday
        [-2, -1],  # Thursday
        [-2, -1],  # Friday
    ]
    # 周末不考虑
    if weekday > 4:
        raise ValueError("ArXiv 不在周末更新")

    delta = delta_list[weekday]

    start_time = (target_date + timedelta(days=delta[0])).replace(hour=19, minute=0, second=0, microsecond=0)
    end_time = (target_date + timedelta(days=delta[1])).replace(hour=19, minute=0, second=0, microsecond=0)

    return start_time, end_time


def get_last_n_days_arxiv_time_range(n_days=7):
    """
    获取过去 n_days 天的 arXiv 时间区间。
    每天时间区间为 UTC 19:00 到次日 19:00。
    :param n_days: 回溯天数
    :return: (start_time, end_time) datetime 对象
    """
    current_time = datetime.now(timezone.utc)

    start_times = []
    end_times = []

    for i in range(n_days):
        date = current_time - timedelta(days=i)
        start_time = (date - timedelta(days=1)).replace(hour=19, minute=0, second=0, microsecond=0)
        end_time = date.replace(hour=19, minute=0, second=0, microsecond=0)
        start_times.append(start_time)
        end_times.append(end_time)

    return min(start_times), max(end_times) if start_times else (None, None)


def format_time_range(start_time, end_time):
    """
    将时间格式化为字符串 'YYYY-MM-DD HH:MM:SS'，与数据库时间格式一致
    """
    return start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    # 获取最新论文时间区间
    start_time, end_time = get_new_papers_date()
    print(f"Start: {start_time.date()} 星期{start_time.weekday() + 1}")
    print(f"End: {end_time.date()} 星期{end_time.weekday() + 1}")
    print("Start time:", start_time)
    print("End time:", end_time)

    start_str, end_str = format_time_range(start_time, end_time)
    print("Formatted Start time:", start_str)
    print("Formatted End time:", end_str)

    # 获取过去 7 天时间区间
    last_week_start, last_week_end = get_last_n_days_arxiv_time_range(7)
    print("Last 7 days range:", last_week_start, "to", last_week_end)
