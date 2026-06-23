# -*- coding: utf-8 -*-
"""
knowledge_updater.py - SECOND-KNOWLEDGE-BRAIN crawler for dating-relationship-strategy-analyzer.

Production pipeline:
- PubMed (NCBI E-utilities)
- Semantic Scholar
- Crossref
- arXiv

Queries authoritative sources for relationship-science literature, scores entries by
recency and domain relevance, deduplicates by DOI/URL hash, and appends dated entries
to SECOND-KNOWLEDGE-BRAIN.md.
"""
import argparse
import asyncio
import datetime
import hashlib
import json
import logging
import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Set
from urllib.parse import quote_plus

import httpx

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BRAIN = os.path.join(HERE, "..", "SECOND-KNOWLEDGE-BRAIN.md")

SOURCES = [
    "PubMed / PsycINFO",
    "Semantic Scholar",
    "Crossref",
    "arXiv"
]

QUERIES = [
    "attachment style relationship outcomes",
    "Gottman four horsemen predictive validity",
    "online dating profile authenticity",
    "communication patterns relationship satisfaction",
    "adult romantic attachment meta-analysis",
    "nonviolent communication conflict resolution"
]

DOMAIN_KEYWORDS = [
    "attachment",
    "gottman",
    "four horsemen",
    "communication",
    "compatibility",
    "authenticity",
    "emotional safety",
    "clarity",
    "nonviolent communication",
    "relationship satisfaction"
]

logger = logging.getLogger("knowledge_updater")


def _hash(url: str, title: str = "") -> str:
    key = (url or title or "").strip().lower()
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def load_existing_hashes(path: str) -> Set[str]:
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return set(re.findall(r"<!--hash:([0-9a-f]{16})-->", text))


def _parse_year(value: Any) -> Optional[int]:
    if not value:
        return None
    if isinstance(value, int):
        return value
    m = re.search(r"(19|20)[0-9][0-9]", str(value))
    return int(m.group(0)) if m else None


def score_entry(entry: Dict[str, Any]) -> float:
    year = _parse_year(entry.get("year"))
    now = datetime.date.today().year
    if year:
        recency = max(0.0, 1.0 - (now - year) / 15.0)
    else:
        recency = 0.3
    text = f"{entry.get('title', '')} {entry.get('abstract', '')} {entry.get('venue', '')}".lower()
    hits = sum(1 for k in DOMAIN_KEYWORDS if k in text)
    relevance = min(1.0, hits / max(1, len(DOMAIN_KEYWORDS) / 3))
    return round(0.5 * recency + 0.5 * relevance, 3)


def _atom_text(element: ET.Element, tag: str) -> str:
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    child = element.find(f"atom:{tag}", ns)
    return (child.text or "").strip() if child is not None else ""


class Crawler:
    def __init__(self, client: httpx.AsyncClient, ncbi_api_key: Optional[str] = None):
        self.client = client
        self.ncbi_api_key = ncbi_api_key

    async def _ncbi_rate_limit(self):
        delay = 0.1 if self.ncbi_api_key else 0.34
        await asyncio.sleep(delay)

    async def search_pubmed(self, query: str, since: Optional[datetime.date], max_results: int) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        term = quote_plus(query)
        mindate = since.strftime("%Y/%m/%d") if since else "2000/01/01"
        esearch_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            f"?db=pubmed&term={term}&retmax={max_results}&sort=date&retmode=json"
            f"&mindate={mindate}&datetype=pdat"
        )
        if self.ncbi_api_key:
            esearch_url += f"&api_key={self.ncbi_api_key}"
        await self._ncbi_rate_limit()
        try:
            r = await self.client.get(esearch_url, timeout=30.0)
            r.raise_for_status()
            data = r.json()
        except Exception as exc:
            logger.warning("PubMed esearch failed for %r: %s", query, exc)
            return results
        ids = data.get("esearchresult", {}).get("idlist", [])
        if not ids:
            return results
        id_str = ",".join(ids)
        esummary_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            f"?db=pubmed&id={id_str}&retmode=json"
        )
        if self.ncbi_api_key:
            esummary_url += f"&api_key={self.ncbi_api_key}"
        await self._ncbi_rate_limit()
        try:
            r = await self.client.get(esummary_url, timeout=30.0)
            r.raise_for_status()
            summaries = r.json().get("result", {})
        except Exception as exc:
            logger.warning("PubMed esummary failed: %s", exc)
            return results
        for uid in ids:
            doc = summaries.get(uid, {})
            if not isinstance(doc, dict):
                continue
            title = doc.get("title", "")
            authors = ", ".join(a.get("name", "") for a in doc.get("authors", []))
            year = _parse_year(doc.get("pubdate"))
            venue = doc.get("fulljournalname", "") or doc.get("source", "")
            doi = ""
            for aid in doc.get("articleids", []):
                if aid.get("idtype") == "doi":
                    doi = aid.get("value", "")
                    break
            url = f"https://doi.org/{doi}" if doi else f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
            abstract = doc.get("abstracttext", "") or ""
            if since and year and year < since.year:
                continue
            results.append({
                "title": title, "authors": authors, "year": year, "venue": venue,
                "doi": doi, "url": url, "abstract": abstract, "source": "PubMed"
            })
        return results

    async def search_semantic_scholar(self, query: str, since: Optional[datetime.date], max_results: int) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        fields = "title,authors,year,venue,abstract,externalIds,url"
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={quote_plus(query)}&fields={fields}&limit={max_results}"
        )
        try:
            r = await self.client.get(url, timeout=30.0)
            r.raise_for_status()
            data = r.json()
        except Exception as exc:
            logger.warning("Semantic Scholar search failed for %r: %s", query, exc)
            return results
        for paper in data.get("data", []):
            year = paper.get("year")
            if since and isinstance(year, int) and year < since.year:
                continue
            authors = ", ".join(a.get("name", "") for a in paper.get("authors", []))
            ext = paper.get("externalIds") or {}
            doi = ext.get("doi", "")
            url_paper = paper.get("url") or (f"https://doi.org/{doi}" if doi else "")
            results.append({
                "title": paper.get("title", ""),
                "authors": authors,
                "year": year,
                "venue": paper.get("venue", "Semantic Scholar"),
                "doi": doi,
                "url": url_paper,
                "abstract": paper.get("abstract", "") or "",
                "source": "Semantic Scholar"
            })
        return results

    async def search_crossref(self, query: str, since: Optional[datetime.date], max_results: int) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        since_str = since.isoformat() if since else "2000-01-01"
        url = (
            "https://api.crossref.org/works"
            f"?query={quote_plus(query)}&filter=from-pub-date:{since_str}"
            f"&rows={max_results}&sort=published&order=desc"
        )
        try:
            r = await self.client.get(url, timeout=30.0)
            r.raise_for_status()
            items = r.json().get("message", {}).get("items", [])
        except Exception as exc:
            logger.warning("Crossref search failed for %r: %s", query, exc)
            return results
        for item in items:
            year = None
            for date_key in ("published-print", "published-online", "created"):
                dp = item.get(date_key, {}).get("date-parts")
                if dp and isinstance(dp, list) and dp[0]:
                    year = int(dp[0][0]) if str(dp[0][0]).isdigit() else None
                    break
            if not year:
                year = _parse_year(item.get("published-print") or item.get("published-online"))
            if since and year and year < since.year:
                continue
            authors = ", ".join(
                f"{a.get('given', '')} {a.get('family', '')}".strip()
                for a in item.get("author", [])
            )
            title = " ".join(item.get("title", []))
            venue = " ".join(item.get("container-title", []))
            doi = item.get("DOI", "")
            url = item.get("URL") or (f"https://doi.org/{doi}" if doi else "")
            results.append({
                "title": title, "authors": authors, "year": year, "venue": venue,
                "doi": doi, "url": url, "abstract": item.get("abstract", "") or "",
                "source": "Crossref"
            })
        return results

    async def search_arxiv(self, query: str, since: Optional[datetime.date], max_results: int) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        url = (
            "http://export.arxiv.org/api/query"
            f"?search_query=all:{quote_plus(query)}&start=0&max_results={max_results}"
            "&sortBy=submittedDate&sortOrder=descending"
        )
        try:
            r = await self.client.get(url, timeout=30.0)
            r.raise_for_status()
            root = ET.fromstring(r.text)
        except Exception as exc:
            logger.warning("arXiv search failed for %r: %s", query, exc)
            return results
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title = _atom_text(entry, "title")
            if "withdrawn" in title.lower():
                continue
            published = _atom_text(entry, "published")
            year = _parse_year(published)
            if since and year and year < since.year:
                continue
            authors = ", ".join(a.text for a in entry.findall("atom:author/atom:name", ns) if a.text)
            summary = _atom_text(entry, "summary")
            entry_id = _atom_text(entry, "id")
            link = entry.find("atom:link[@rel='alternate']", ns)
            url = link.attrib.get("href") if link is not None else entry_id
            results.append({
                "title": title, "authors": authors, "year": year, "venue": "arXiv preprint",
                "doi": "", "url": url, "abstract": summary, "source": "arXiv"
            })
            await asyncio.sleep(0.05)
        return results


async def crawl_sources(
    queries: List[str],
    since: Optional[datetime.date],
    max_results: int,
    ncbi_api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    limits = httpx.Limits(max_connections=10)
    transport = httpx.AsyncHTTPTransport(retries=3)
    entries: List[Dict[str, Any]] = []
    async with httpx.AsyncClient(timeout=30.0, limits=limits, transport=transport) as client:
        crawler = Crawler(client, ncbi_api_key=ncbi_api_key)
        coros = []
        for q in queries:
            coros.append(crawler.search_pubmed(q, since, max_results))
            coros.append(crawler.search_semantic_scholar(q, since, max_results))
            coros.append(crawler.search_crossref(q, since, max_results))
            coros.append(crawler.search_arxiv(q, since, max_results))
        batches = await asyncio.gather(*coros, return_exceptions=True)
    for batch in batches:
        if isinstance(batch, Exception):
            logger.warning("Source batch failed: %s", batch)
            continue
        entries.extend(batch)
    return entries


def append_entries(entries: List[Dict[str, Any]], path: str) -> int:
    existing = load_existing_hashes(path)
    added = 0
    lines: List[str] = []
    today = datetime.date.today().isoformat()
    for e in sorted(entries, key=score_entry, reverse=True):
        h = _hash(e.get("url", ""), e.get("title", ""))
        if h in existing:
            continue
        sc = score_entry(e)
        doi = e.get("doi", "")
        url = e.get("url", "")
        link = url or (f"https://doi.org/{doi}" if doi else "")
        lines.append(
            f"- {today} | score={sc} | **{e.get('title','')}** | {e.get('authors','')} "
            f"| {e.get('year','n.d.')} | {e.get('venue','')} | {link} "
            f"| {e.get('abstract','')[:200]}... <!--hash:{h}-->"
        )
        existing.add(h)
        added += 1
    if added:
        header = f"\n### Crawl {today} (+{added})\n"
        with open(path, "a", encoding="utf-8") as f:
            f.write(header + "\n".join(lines) + "\n")
    logger.info("Appended %d new entries to %s", added, path)
    return added


def _load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Update SECOND-KNOWLEDGE-BRAIN.md with fresh relationship-science literature.")
    ap.add_argument("--brain", default=DEFAULT_BRAIN, help="Path to SECOND-KNOWLEDGE-BRAIN.md")
    ap.add_argument("--since", type=str, help="ISO date floor (YYYY-MM-DD)")
    ap.add_argument("--max-results", type=int, default=10, help="Max results per source per query")
    ap.add_argument("--dry-run", action="store_true", help="Print entries without writing")
    ap.add_argument("--config", type=str, help="JSON config with sources/queries/keywords")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    since = datetime.date.fromisoformat(args.since) if args.since else None
    queries = QUERIES
    ncbi_key = os.environ.get("NCBI_API_KEY")

    if args.config:
        cfg = _load_config(args.config)
        queries = cfg.get("queries", queries)
        ncbi_key = cfg.get("ncbi_api_key") or ncbi_key

    entries = asyncio.run(crawl_sources(queries, since, args.max_results, ncbi_key))

    if args.dry_run:
        print(json.dumps([{**e, "score": score_entry(e)} for e in entries], indent=2, default=str)[:4000])
        return 0

    append_entries(entries, args.brain)
    return 0


if __name__ == "__main__":
    sys.exit(main())
