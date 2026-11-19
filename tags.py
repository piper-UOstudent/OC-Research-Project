# Aided by Gemini 
from pytumblr_master import pytumblr
import pandas as pd
from collections import Counter
import re


client = pytumblr.TumblrRestClient(
    # redacted for public postiing
)

# Make the request
client.info()

def fetch_oc_posts(tag="original character", limit=400):
    posts_data = []
    # Fetching posts tagged with the search term
    # Note: Tumblr API allows pagination using 'before' timestamps if needed
    response = client.tagged(tag, limit=20)
    
    for post in response:
        # Extract basic info
        blog_name = post.get('blog_name')
        tags = post.get('tags', [])
        summary = post.get('summary', '')
        body = post.get('body', '')
        note_count = post.get('note_count', 0)
        
        posts_data.append({
            'blog_name': blog_name,
            'tags': tags,
            'note_count': note_count,
            'text_content': summary + " " + body
        })
        
    return pd.DataFrame(posts_data)


def analyze_tags(df):
    all_tags = [tag.lower() for sublist in df['tags'] for tag in sublist]
    tag_counts = Counter(all_tags)
    
    # Exclude the search term itself if it dominates
    tag_counts.pop('original character', None)
    tag_counts.pop('oc', None)
    
    print("--- Top 10 Co-occurring Tags ---")
    for tag, count in tag_counts.most_common(10):
        print(f"#{tag}: {count} posts")


df = fetch_oc_posts()
analyze_tags(df)
