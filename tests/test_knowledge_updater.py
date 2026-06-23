import json
import os
import tempfile
from datetime import date
from pathlib import Path

import httpx
import pytest

from tools import knowledge_updater as ku

FIXTURES = Path(__file__).parent / "fixtures"


def test_hash_is_stable_and_deterministic():
    h1 = ku._hash("https://doi.org/10.1234/example", "Title")
    h2 = ku._hash("https://doi.org/10.1234/example", "Title")
    assert h1 == h2
    assert len(h1) == 16


def test_score_entry_prefers_recent_relevant_papers():
    ancient = {"title": "Ancient history", "year": 1990, "abstract": "", "venue": ""}
    fresh = {
        "title": "attachment style relationship outcomes meta-analysis",
        "year": date.today().year,
        "abstract": "Gottman communication patterns",
        "venue": "Journal of Social and Personal Relationships"
    }
    assert ku.score_entry(fresh) > ku.score_entry(ancient)


def test_load_existing_hashes_extracts_hashes():
    text = "- entry <!--hash:deadbeef01234567--> and <!--hash:abcdef0123456789-->"
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    try:
        assert ku.load_existing_hashes(path) == {"deadbeef01234567", "abcdef0123456789"}
    finally:
        os.unlink(path)


def test_append_entries_dedups_and_appends():
    old_hash = ku._hash("http://old")
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md", encoding="utf-8") as f:
        f.write(f"# Brain\n\n### Log\n- 2026-01-01 | **Old** | <!--hash:{old_hash}-->\n")
        path = f.name
    try:
        entries = [
            {"title": "Old", "url": "http://old", "year": 2025, "abstract": "", "venue": ""},
            {"title": "New", "url": "http://new", "year": 2026, "abstract": "attachment", "venue": ""},
        ]
        added = ku.append_entries(entries, path)
        assert added == 1
        content = Path(path).read_text(encoding="utf-8")
        assert "New" in content
        assert content.count("Old") == 1
    finally:
        os.unlink(path)


def test_parse_year_handles_variants():
    assert ku._parse_year("2023 Jan 15") == 2023
    assert ku._parse_year(2020) == 2020
    assert ku._parse_year("n.d.") is None
    assert ku._parse_year(None) is None


@pytest.mark.asyncio
async def test_search_pubmed_parses_mock_response():
    esearch_payload = {"esearchresult": {"idlist": ["12345"]}}
    esummary_payload = {"result": {"12345": {
        "title": "Attachment and relationships",
        "authors": [{"name": "Smith, J"}],
        "pubdate": "2024 Jan",
        "fulljournalname": "J Pers Soc Psychol",
        "articleids": [{"idtype": "doi", "value": "10.1234/example"}],
        "abstracttext": "Abstract text here."
    }, "uids": ["12345"]}}

    def handler(request: httpx.Request):
        url = str(request.url)
        if "esearch" in url:
            return httpx.Response(200, json=esearch_payload)
        if "esummary" in url:
            return httpx.Response(200, json=esummary_payload)
        return httpx.Response(404)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    crawler = ku.Crawler(client)
    results = await crawler.search_pubmed("attachment", None, 5)
    assert len(results) == 1
    assert results[0]["title"] == "Attachment and relationships"
    assert results[0]["doi"] == "10.1234/example"
    await client.aclose()


@pytest.mark.asyncio
async def test_search_semantic_scholar_parses_mock_response():
    payload = {"data": [{
        "title": "Gottman horsemen study",
        "authors": [{"name": "Gottman, J"}],
        "year": 2024,
        "venue": "J Fam Psychol",
        "abstract": "communication patterns",
        "externalIds": {"doi": "10.5678/x"},
        "url": "https://example.org/x"
    }]}

    def handler(request: httpx.Request):
        return httpx.Response(200, json=payload)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    crawler = ku.Crawler(client)
    results = await crawler.search_semantic_scholar("Gottman", None, 5)
    assert len(results) == 1
    assert results[0]["source"] == "Semantic Scholar"
    assert results[0]["doi"] == "10.5678/x"
    await client.aclose()


@pytest.mark.asyncio
async def test_search_crossref_parses_mock_response():
    payload = {"message": {"items": [{
        "title": ["Love and compatibility"],
        "author": [{"given": "A", "family": "Researcher"}],
        "published-print": {"date-parts": [[2024]]},
        "container-title": ["J Relat Sci"],
        "DOI": "10.9999/love",
        "URL": "https://doi.org/10.9999/love",
        "abstract": "Compatibility research abstract"
    }]}}

    def handler(request: httpx.Request):
        return httpx.Response(200, json=payload)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    crawler = ku.Crawler(client)
    results = await crawler.search_crossref("compatibility", None, 5)
    assert len(results) == 1
    assert results[0]["doi"] == "10.9999/love"
    await client.aclose()


@pytest.mark.asyncio
async def test_search_arxiv_parses_mock_response():
    atom = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Attachment in online dating</title>
    <author><name>Jane Doe</name></author>
    <published>2024-03-15T00:00:00Z</published>
    <summary>Study of authenticity in dating profiles.</summary>
    <id>http://arxiv.org/abs/2403.00001</id>
    <link rel="alternate" href="http://arxiv.org/abs/2403.00001" />
  </entry>
</feed>"""

    def handler(request: httpx.Request):
        return httpx.Response(200, text=atom)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    crawler = ku.Crawler(client)
    results = await crawler.search_arxiv("online dating", None, 5)
    assert len(results) == 1
    assert results[0]["title"] == "Attachment in online dating"
    assert results[0]["year"] == 2024
    await client.aclose()


def test_main_dry_run_runs_without_error(monkeypatch):
    async def fake_crawl(*args, **kwargs):
        return [{"title": "Test", "url": "http://test", "year": 2024, "abstract": "attachment", "venue": ""}]
    monkeypatch.setattr(ku, "crawl_sources", fake_crawl)
    assert ku.main(["--dry-run"]) == 0
