import json
from urllib import request, error
from typing import List, Dict, Optional

BASE_URL = "https://hacker-news.firebaseio.com/v0"

def fetch_item(item_id: int) -> Optional[Dict]:
    """Fetch a single item from HackerNews API"""
    try:
        url = f"{BASE_URL}/item/{item_id}.json"
        with request.urlopen(url) as response:
            return json.loads(response.read())
    except (error.URLError, json.JSONDecodeError):
        return None

def fetch_top_stories(limit: int = 5) -> List[Dict]:
    """Fetch top stories from HackerNews"""
    try:
        # Get top stories IDs
        url = f"{BASE_URL}/topstories.json"
        with request.urlopen(url) as response:
            story_ids = json.loads(response.read())

        # Fetch details for each story
        stories = []
        for story_id in story_ids[:limit]:
            story = fetch_item(story_id)
            if story:
                stories.append(story)

        return stories
    except (error.URLError, json.JSONDecodeError):
        return []

def get_hackernews_info(query: str) -> str:
    """Process user query and return HackerNews information"""
    # Default to 5 stories if no number specified
    limit = 5

    # Check if user specified a number of stories
    words = query.lower().split()
    try:
        if 'top' in words and len(words) > words.index('top') + 1:
            limit = int(words[words.index('top') + 1])
            limit = min(limit, 20)  # Cap at 20 stories
    except ValueError:
        pass

    stories = fetch_top_stories(limit)
    if not stories:
        return "Sorry, I couldn't fetch stories from HackerNews"

    response = f"Top {len(stories)} stories from HackerNews:\n\n"
    for i, story in enumerate(stories, 1):
        title = story.get('title', 'No title')
        author = story.get('by', 'unknown')
        url = story.get('url', '')

        response += f"{i}. {title}\n"
        response += f"   Author: {author}\n"
        if url:
            response += f"   URL: {url}\n"

    return response