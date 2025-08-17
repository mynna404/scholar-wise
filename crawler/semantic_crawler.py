import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from models.paper_info import PaperInfo


def get_ui_version(session):
    url = "https://www.semanticscholar.org/"
    resp = session.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/139.0.0.0 Safari/537.36"
    })

    if resp.status_code != 200:
        raise Exception(f"获取主页失败: {resp.status_code}")

    soup = BeautifulSoup(resp.text, "html.parser")
    tag = soup.find("meta", attrs={"name": "s2-ui-version"})
    if not tag:
        raise Exception("未找到 meta[name='s2-ui-version']")
    return tag.get("content")


def search_semantic_scholar(query, page=1, page_size=10):
    session = requests.Session()
    ui_version = get_ui_version(session)

    url = "https://www.semanticscholar.org/api/1/search"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://www.semanticscholar.org",
        "referer": f"https://www.semanticscholar.org/search?q={query}&sort=relevance",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/139.0.0.0 Safari/537.36",
        "x-s2-client": "webapp-browser",
        "x-s2-ui-version": ui_version,
    }

    payload = {
        "queryString": query,
        "page": page,
        "pageSize": page_size,
        "sort": "relevance",
        "authors": [],
        "coAuthors": [],
        "venues": [],
        "yearFilter": None,
        "requireViewablePdf": False,
        "fieldsOfStudy": [],
        "hydrateWithDdb": True,
        "includeTldrs": True,
        "performTitleMatch": True,
        "includeBadges": True,
        "getQuerySuggestions": False,
        "cues": [
            "CitedByLibraryPaperCue",
            "CitesYourPaperCue",
            "CitesLibraryPaperCue"
        ],
        "includePdfVisibility": True
    }

    resp = session.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise Exception(f"请求失败: {resp.status_code}, {resp.text}")

    return resp.json()


def json_to_paper(json: Dict[str, Any]) -> List[PaperInfo]:
    """把搜索结果转换成 PaperInfo 列表"""
    return [PaperInfo.from_raw(p) for p in json.get("results", [])]


def search(query, page, page_size):
    raw_json = search_semantic_scholar(query, page=page, page_size=page_size)
    return json_to_paper(raw_json)


if __name__ == "__main__":
    paper_name = input("请输入论文名称: ")
    data = search_semantic_scholar(paper_name, page=1, page_size=5)

    papers = json_to_paper(data)

    for idx, paper in enumerate(papers, 1):
        print(f"====== Paper {idx} ======")
        print(paper)
