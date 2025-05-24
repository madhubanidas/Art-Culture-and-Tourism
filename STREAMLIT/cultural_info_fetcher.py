import wikipediaapi
import time
import re

def clean_text(text):
    """Clean Wikipedia text"""
    text = re.sub(r'\([^)]*\)', '', text)  
    text = re.sub(r'\[[^\]]*\]', '', text)  
    text = ' '.join(text.split())  
    return text.strip()


def get_cultural_info(Destination, State):
    wiki_wiki = wikipediaapi.Wikipedia(
       language='en',
        user_agent='STREAMLIT/1.0 (contact: madhubanidas@gmail.com)', 
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    
    
    # Try different search patterns
    search_queries = [
        f"{Destination}, {State}",
        Destination,
        f"{Destination} (India)"
    ]
    
    for query in search_queries:
        page = wiki_wiki.page(query)
        if page.exists():
            summary = clean_text(page.summary[0:500])  
            return f"{summary}... [Read more on Wikipedia]({page.fullurl})"
        time.sleep(1)  
    
    return "Cultural information not available. Consider adding manually."

