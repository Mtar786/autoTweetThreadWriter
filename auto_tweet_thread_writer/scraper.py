"""Web scraping utilities for the Auto Tweet Thread Writer.

This module defines functions to fetch and extract text content from a URL.
It uses :mod:`requests` to download the page and :mod:`BeautifulSoup` to
parse the HTML.  The primary function, :func:`fetch_content`, returns the
page title, meta description and concatenated paragraph text.  It works
reasonably well for simple blog posts and video landing pages.
"""

from __future__ import annotations

import logging
from typing import Tuple

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def fetch_content(url: str) -> Tuple[str, str, str]:
    """Fetch the HTML at ``url`` and extract its title, description and text.

    Parameters
    ----------
    url : str
        The URL to fetch.

    Returns
    -------
    tuple of (title, description, content)
        ``title`` is the page's `<title>` text if present.
        ``description`` is the `<meta name="description">` content.
        ``content`` is the concatenated text of all `<p>` elements on the page.

    Notes
    -----
    This function does not execute JavaScript.  It may not work correctly on
    highly dynamic pages.  For videos without transcripts, the description
    usually contains a useful summary.
    """
    logger.debug("Fetching URL: %s", url)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Extract title
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    # Extract meta description
    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        description = meta_desc["content"].strip()
    # Extract paragraphs
    paragraphs = []
    for p in soup.find_all("p"):
        text = p.get_text(separator=" ", strip=True)
        if text:
            paragraphs.append(text)
    content = "\n".join(paragraphs)
    return title, description, content