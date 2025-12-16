"""Command‑line interface for the Auto Tweet Thread Writer.

Execute as ``python -m auto_tweet_thread_writer.cli``.  Provide a URL, and
the script will fetch the page, summarise it, and output a thread of
tweets.  You may optionally save the output to a file.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

from .writer import generate_thread


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Twitter thread from a URL.")
    parser.add_argument("url", type=str, help="URL of the blog post or video page to summarise")
    parser.add_argument(
        "--output",
        type=str,
        help="Path to write the thread (optional). If not provided, prints to stdout.",
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Optional override for the thread title (used in the hook).",
    )
    parser.add_argument(
        "--openai-api-key",
        dest="openai_api_key",
        type=str,
        default=os.getenv("OPENAI_API_KEY"),
        help="OpenAI API key for summarisation (optional)",
    )
    parser.add_argument(
        "--max-tweets",
        dest="max_tweets",
        type=int,
        default=10,
        help="Number of tweets to generate (default: 10)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    try:
        tweets = generate_thread(
            url=args.url,
            openai_api_key=args.openai_api_key,
            title=args.title,
            max_tweets=args.max_tweets,
        )
    except Exception as exc:
        print(f"Error generating thread: {exc}", file=sys.stderr)
        return 1
    content = "\n\n".join(tweets)
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Thread saved to {args.output}")
        except Exception as exc:
            print(f"Error writing file: {exc}", file=sys.stderr)
            return 1
    else:
        print(content)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())