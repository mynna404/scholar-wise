from typing import List, Optional

from crawler import semantic_crawler
from models.paper_info import PaperInfo


class PaperService:

    @staticmethod
    def search_papers(query: str, page: int = 1, page_size: int = 10) -> List[PaperInfo]:
        return semantic_crawler.search(query, page, page_size)

    @staticmethod
    def get_paper_detail(paper_id: str) -> Optional[PaperInfo]:
        pass

    @staticmethod
    def get_paper_pdf_url(paper_id: str) -> Optional[str]:
        pass
