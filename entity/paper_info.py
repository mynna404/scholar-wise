from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class PaperInfo:
    """论文真实信息类"""
    id: Optional[str] = None
    corpusId: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[str] = None
    year: Optional[int] = None
    venue: Optional[str] = None
    tldr: Optional[str] = None
    citations: Optional[int] = None
    pdf_url: Optional[str] = None

    @classmethod
    def from_raw(cls, raw: Dict[str, Any]) -> "PaperInfo":
        """从原始 API/JSON 数据解析出 PaperInfo"""
        authors = "; ".join(
            f"{a.get('firstName', '')} "
            f"{a['middleNames'][0] if a.get('middleNames') else ''} "
            f"{a.get('lastName', '')}".strip()
            for a in raw.get("structuredAuthors", [])
        ) or None

        return cls(
            id=raw.get("id"),
            corpusId=raw.get("corpusId"),
            title=raw.get("title", {}).get("text"),
            authors=authors,
            year=int(raw.get("year", {}).get("text") or 0) if raw.get("year") else None,
            venue=raw.get("venue", {}).get("text") or raw.get("journal", {}).get("name"),
            tldr=raw.get("tldr", {}).get("text"),
            citations=raw.get("citationStats", {}).get("numCitations"),
            pdf_url=(
                raw.get("openAccessInfo", {}).get("location", {}).get("url")
                or raw.get("primaryPaperLink", {}).get("url")
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转成 dict"""
        return {
            "id": self.id,
            "corpusId": self.corpusId,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "venue": self.venue,
            "tldr": self.tldr,
            "citations": self.citations,
            "pdf_url": self.pdf_url,
        }

    def __str__(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"CorpusID: {self.corpusId}\n"
            f"Title: {self.title}\n"
            f"Authors: {self.authors}\n"
            f"Year: {self.year}\n"
            f"Venue: {self.venue}\n"
            f"TL;DR: {self.tldr}\n"
            f"Citations: {self.citations}\n"
            f"PDF URL: {self.pdf_url}\n"
        )