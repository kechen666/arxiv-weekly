from datetime import datetime, timedelta, timezone
import arxiv
from config import FIELD_CATEGORY_KEYWORDS, TEAM_CATEGORY_KEYWORDS, DEFAULT_KEYWORD
from utility import get_last_n_days_arxiv_time_range

def get_papers(start_time, end_time, keyword=DEFAULT_KEYWORD, max_results=400, sort_by="submitted_date"):
    """Fetch daily papers from arXiv without storing to DB."""
    try:
        client = arxiv.Client()
        start_time_str = start_time.strftime("%Y%m%d%H%M")
        end_time_str = end_time.strftime("%Y%m%d%H%M")
        print(f"Searching for papers with keyword '{keyword}' from {start_time_str} to {end_time_str}...")

        query = f"all:{keyword} AND submittedDate:[{start_time_str} TO {end_time_str}]"
        # 优先级设置
        sort_criterion = {
            "relevance": arxiv.SortCriterion.Relevance,
            "last_updated_date": arxiv.SortCriterion.LastUpdatedDate,
            "submitted_date": arxiv.SortCriterion.SubmittedDate
        }.get(sort_by, arxiv.SortCriterion.SubmittedDate)

        search = arxiv.Search(query=query, max_results=max_results, sort_by=sort_criterion)

        papers = []
        for result in client.results(search):
            papers.append({
                "title": result.title,
                "authors": [str(a.name) for a in result.authors],
                "published": result.published,
                "url": result.entry_id,
                "summary": result.summary,
                "primary_category": result.primary_category
            })
        print(f"Found {len(papers)} papers.")
        return papers
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return []

def filter_papers_by_field_in_list(papers, field_category):
    """
    筛选 papers 中与 field_category 相关的论文（标题或 primary_category 包含任意关键词）。
    :param papers: list of paper dicts
    :param field_category: FIELD_CATEGORY_KEYWORDS 中的 key
    :return: 筛选后的 papers 列表
    """
    if field_category not in FIELD_CATEGORY_KEYWORDS:
        raise ValueError(f"{field_category} not in FIELD_CATEGORY_KEYWORDS")

    keywords = FIELD_CATEGORY_KEYWORDS[field_category]
    filtered = [
        p for p in papers
        if any(k.lower() in p['summary'].lower() or k.lower() in p['title'].lower() for k in keywords)
    ]
    return filtered


def filter_papers_by_team_in_list(papers, team_category):
    """
    筛选 papers 中由 team_category 相关人员贡献的论文（authors 包含任意关键词）。
    :param papers: list of paper dicts
    :param team_category: TEAM_CATEGORY_KEYWORDS 中的 key
    :return: 筛选后的 papers 列表
    """
    if team_category not in TEAM_CATEGORY_KEYWORDS:
        raise ValueError(f"{team_category} not in TEAM_CATEGORY_KEYWORDS")

    keywords = TEAM_CATEGORY_KEYWORDS[team_category]
    filtered = [
        p for p in papers
        if any(any(k.lower() in a.lower() for a in p['authors']) for k in keywords)
    ]
    return filtered


def print_papers_by_field_in_list(papers):
    """
    遍历 FIELD_CATEGORY_KEYWORDS 中的所有领域，并打印匹配的论文。
    改进版打印，便于 Windows 终端阅读。
    """
    for field in FIELD_CATEGORY_KEYWORDS.keys():
        filtered = filter_papers_by_field_in_list(papers, field)
        if filtered:
            print("=" * 80)
            print(f"[FIELD] {field} papers".center(80))
            print("-" * 80)
            for idx, paper in enumerate(filtered, 1):
                pub_date = paper['published'].strftime("%Y-%m-%d")
                print(f"[{idx}] Title   : {paper['title']}")
                print(f"     Authors : {', '.join(paper['authors'])}")
                print(f"     Date    : {pub_date}")
                print(f"     Category: {paper['primary_category']}")
                print(f"     URL     : {paper['url']}")
                print("-" * 80)


def print_papers_by_team_in_list(papers):
    """
    遍历 TEAM_CATEGORY_KEYWORDS 中的所有团队，并打印团队成员相关的论文。
    改进版打印，便于 Windows 终端阅读。
    """
    for team in TEAM_CATEGORY_KEYWORDS.keys():
        filtered = filter_papers_by_team_in_list(papers, team)
        if filtered:
            print("=" * 80)
            print(f"[TEAM] {team} team papers".center(80))
            print("-" * 80)
            for idx, paper in enumerate(filtered, 1):
                pub_date = paper['published'].strftime("%Y-%m-%d")
                print(f"[{idx}] Title   : {paper['title']}")
                print(f"     Authors : {', '.join(paper['authors'])}")
                print(f"     Date    : {pub_date}")
                print(f"     Category: {paper['primary_category']}")
                print(f"     URL     : {paper['url']}")
                print("-" * 80)



if __name__ == "__main__":
    start, end = get_last_n_days_arxiv_time_range(7)
    start_str = start.strftime("%Y-%m-%d %H:%M")
    end_str = end.strftime("%Y-%m-%d %H:%M")
    
    print("=" * 80)
    print(f"Fetching papers from {start_str} to {end_str}...".center(80))
    print("=" * 80)

    # 从 config 获取默认 keyword
    keyword = DEFAULT_KEYWORD if DEFAULT_KEYWORD else "quantum"

    papers = get_papers(start_time=start, end_time=end, keyword=keyword)

    print("=" * 80)
    if papers:
        print(f"Finish fetching {len(papers)} papers.".center(80))
        print("=" * 80)
        print_papers_by_field_in_list(papers)
        print_papers_by_team_in_list(papers)
    else:
        print("No papers found in this time range.".center(80))
        print("=" * 80)

