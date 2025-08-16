from typing import Dict, Any

class PaperInfo:
    """论文信息类"""

    def __init__(self, raw: Dict[str, Any]):
        self.id = raw.get("id")
        self.corpusId = raw.get("corpusId")
        self.title = raw.get("title", {}).get("text")
        self.authors = "; ".join(
            f"{a['firstName']} {a['middleNames'][0] if a['middleNames'] else ''} {a['lastName']}".strip()
            for a in raw.get("structuredAuthors", [])
        )
        self.year = raw.get("year", {}).get("text")
        self.venue = raw.get("venue", {}).get("text") or raw.get("journal", {}).get("name")
        self.tldr = raw.get("tldr", {}).get("text")
        self.citations = raw.get("citationStats", {}).get("numCitations")
        self.pdf_url = (
            raw.get("openAccessInfo", {}).get("location", {}).get("url")
            or raw.get("primaryPaperLink", {}).get("url")
        )

    def __str__(self):
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

    def to_dict(self) -> Dict[str, Any]:
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