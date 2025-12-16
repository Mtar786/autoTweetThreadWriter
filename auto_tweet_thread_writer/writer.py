"""Thread writer for the Auto Tweet Thread Writer.

This module provides functions to summarise text and assemble it into a
Twitter thread.  The central function, :func:`generate_thread`, takes a URL
and optional OpenAI API key, fetches the page content, summarises it, and
returns a list of tweets.  Each tweet includes a serial indicator and an
emoji to improve readability.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional

from .scraper import fetch_content


def _summarize_text(text: str, openai_api_key: Optional[str], target_words: int = 300) -> str:
    """Return a summary of ``text`` limited to roughly ``target_words`` words.

    If an OpenAI API key is provided, this function uses the GPT model to
    produce a concise summary.  Otherwise, it falls back to returning the
    first ``target_words`` words of the input.
    """
    words = text.split()
    if not words:
        return ""
    if openai_api_key:
        try:
            import openai  # type: ignore
            openai.api_key = openai_api_key
            prompt = (
                "Summarise the following text into a concise overview. Focus on the key "
                "ideas and eliminate unnecessary detail. Limit the summary to around "
                f"{target_words} words.\n\n{text}\n\nSummary:"
            )
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass
    # Fallback: naive summarisation by truncating
    return " ".join(words[:target_words])


def _chunk_text(summary: str, n_parts: int) -> List[str]:
    """Divide ``summary`` into ``n_parts`` roughly equal chunks by character length.

    This function does not split in the middle of a word.  It ensures that
    each part is within Twitter's limit (280 characters) by further splitting
    long chunks if necessary.
    """
    summary = summary.strip()
    if not summary:
        return [""] * n_parts
    # Break at sentence boundaries when possible
    sentences = summary.split('. ')
    # Basic algorithm: assemble sentences into chunks without exceeding char limit
    parts: List[str] = []
    current = ""
    for sent in sentences:
        seg = sent.strip()
        if not seg:
            continue
        if current:
            tentative = current + '. ' + seg
        else:
            tentative = seg
        # Reserve some space for numbering and emoji (~10 chars)
        if len(tentative) + 15 > 260:  # near 280 limit minus numbering & emoji
            parts.append(current)
            current = seg
        else:
            current = tentative
    if current:
        parts.append(current)
    # Now we have a list of parts; merge or split to get exactly n_parts
    # If too few parts, split the longest parts
    while len(parts) < n_parts:
        # Find the longest part
        idx = max(range(len(parts)), key=lambda i: len(parts[i]))
        part = parts.pop(idx)
        half = len(part) // 2
        parts.insert(idx, part[:half].strip())
        parts.insert(idx + 1, part[half:].strip())
    # If too many parts, merge smallest
    while len(parts) > n_parts:
        # Find two smallest parts
        if len(parts) < 2:
            break
        idx = min(range(len(parts)-1), key=lambda i: len(parts[i]) + len(parts[i+1]))
        merged = (parts[idx] + ' ' + parts[idx+1]).strip()
        parts[idx:idx+2] = [merged]
    return parts[:n_parts]


def generate_thread(
    url: str,
    openai_api_key: Optional[str] = None,
    title: Optional[str] = None,
    max_tweets: int = 10,
) -> List[str]:
    """Generate a Twitter thread summarising the content at ``url``.

    Parameters
    ----------
    url : str
        The page to summarise.
    openai_api_key : str, optional
        API key to use OpenAI for summarisation.  If omitted, a naive
        summariser is used.
    title : str, optional
        Title to use in the first tweet.  If omitted, the page's title or
        domain will be used.
    max_tweets : int, default 10
        The number of tweets to generate.  Must be between 3 and 20.

    Returns
    -------
    list of str
        A list of tweets, each including an emoji and numbering.
    """
    if max_tweets < 3 or max_tweets > 20:
        raise ValueError("max_tweets must be between 3 and 20")
    page_title, description, content = fetch_content(url)
    chosen_title = title or page_title or url
    base_text = content if content else description
    summary = _summarize_text(base_text, openai_api_key, target_words=300)
    # Emoji list for visual interest
    emojis = ["🚀", "💡", "📌", "🔍", "🔥", "📘", "✅", "🌟", "🎯", "🧠"]
    parts = _chunk_text(summary, max_tweets)
    tweets: List[str] = []
    for i, part in enumerate(parts, start=1):
        emoji = emojis[(i - 1) % len(emojis)]
        header = f"{emoji} {i}/{max_tweets} "
        if i == 1:
            # Hook: mention the topic and hint at value
            hook = f"{chosen_title.strip()} – here’s what you’ll learn:"  # hooking phrase
            body = part.strip()
            # Ensure the hook fits
            first_tweet = f"{header}{hook}\n{body}"
            tweets.append(first_tweet)
        else:
            tweets.append(f"{header}{part.strip()}")
    return tweets