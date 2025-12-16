# Auto‑Tweet Thread Writer

The **Auto‑Tweet Thread Writer** is a utility that transforms long‑form content—such as blog posts or video pages—into a concise, engaging Twitter thread.  Given a URL, the tool fetches and summarises the content, then breaks the summary into a 10‑part thread complete with catchy hooks, numbered tweets, and emojis.  It optionally uses OpenAI to generate higher‑quality summaries and more natural phrasing.

## Features

* **Fetch and parse web pages.**  The script uses `requests` and `BeautifulSoup` to download a blog article or video page and extract textual content.  For videos without transcripts, it falls back to the page’s meta description.
* **Summarise long text.**  The content is summarised into a few paragraphs.  If an OpenAI API key is provided, the summarisation uses a large‑language model; otherwise, it falls back to a simple truncation.
* **Generate a 10‑tweet thread.**  The summary is divided into ten segments.  Each tweet includes an emoji and a serial indicator (e.g., “1/10”).  The first tweet contains a hook to capture attention and hint at the value of the thread, following best practices【449880939810186†L170-L176】【449880939810186†L194-L201】.
* **Write to Markdown.**  The generated thread can be printed to the console or saved to a Markdown file.

## Best practices for Twitter threads

Research shows that Twitter threads often outperform single tweets because they combine storytelling, drama and practical information【449880939810186†L161-L166】.  To maximise engagement:

* **Hook your readers.**  The first line of your thread must grab attention; it functions like a headline—catchy hooks encourage people to read on【449880939810186†L170-L176】.  You can build suspense by mentioning the number of lessons or tips without revealing the main point【449880939810186†L194-L201】.
* **Add concrete examples and visuals.**  Supporting your points with examples, screenshots or links adds proof and helps readers understand nuanced topics【449880939810186†L223-L236】.
* **Be unique.**  Develop a distinctive voice and style to stand out from the crowd; followers appreciate a consistent tone and fresh perspective【449880939810186†L242-L250】.

The generator follows these guidelines by including a hook in the first tweet, using emojis for visual interest, and dividing content evenly across 10 tweets.

## Installation

1. **Clone or download the repository.**
2. **Install dependencies:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   Dependencies include `requests` and `beautifulsoup4` for scraping.  To enable AI‑powered summarisation, install `openai`.

3. **Set your OpenAI API key (optional):**

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

## Usage

Run the CLI with a URL:

```bash
python -m auto_tweet_thread_writer.cli https://example.com/blog-post \
    --output thread.md --openai-api-key $OPENAI_API_KEY
```

Arguments:

| Argument              | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `url`                | The URL of a blog post or video page to summarise.                         |
| `--output`           | Path to write the generated thread (default: print to stdout).            |
| `--title`            | Optional title to override the page title for the opening hook.           |
| `--openai-api-key`   | OpenAI API key (optional). If omitted, a naive summariser is used.        |
| `--max-tweets`       | Number of tweets to generate (default: 10). Must be ≥3 and ≤20.           |

The script outputs each tweet with a number (e.g., `1/10`) and an emoji.  You can copy and paste the result into Twitter’s composer or automate tweeting using another tool.

## Project structure

```
auto_tweet_thread_writer/
├── auto_tweet_thread_writer/
│   ├── __init__.py
│   ├── cli.py         # Command‑line interface
│   ├── scraper.py     # Fetch and parse content from a URL
│   └── writer.py      # Summarise text and assemble a thread
├── requirements.txt
└── README.md
```

## Extending

* **Improve scraping.**  Integrate readability libraries such as `newspaper3k` to get cleaner article text.
* **Add video transcripts.**  Use libraries such as `youtube-transcript-api` to download captions for YouTube videos.
* **Customise style.**  Modify `writer.py` to change the emojis, hook format or tweet segmentation logic.

## License

This project is provided under the MIT License.