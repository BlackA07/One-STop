from supabase import create_client, Client
import re
from typing import List, Dict, Optional

SUPABASE_URL = "https://ifbknohkqfqplwvocksc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmYmtub2hrcWZxcGx3dm9ja3NjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4NjIyMjIsImV4cCI6MjA3NDQzODIyMn0.a5motl3g-arn6B-_JmL4J6WhmwacAkesfW1LnD52FQY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

STOP_WORDS = {
    "kya", "hai", "he", "ka", "ki", "ke", "ko", "se", "me", "mein",
    "what", "is", "the", "a", "an", "of", "define", "explain",
    "tell", "me", "about", "how", "to", "in", "are", "and",
    "or", "but", "for", "on", "with", "as", "by", "from", "do"
}


def extract_keywords(question: str) -> List[str]:
    """Extract meaningful keywords"""
    text = re.sub(r"[^\w\s]", " ", question.lower())
    words = text.split()
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return keywords[:2]


def search_supabase(question: str) -> Optional[Dict]:
    """Search database and return complete info with metadata"""
    try:
        keywords = extract_keywords(question)
        
        if not keywords:
            return None
        
        # Search with first keyword
        query = supabase.table("knowledge").select("text_chunk, subject, source_file")
        query = query.ilike("text_chunk", f"%{keywords[0]}%")
        
        res = query.limit(1).execute()
        
        if not res.data:
            return None
        
        result = res.data[0]
        
        # Clean the text
        text = result['text_chunk']
        cleaned = ' '.join(text.split())
        
        # Take more text (600 characters for better content)
        if len(cleaned) > 600:
            # Find last complete sentence within 600 chars
            truncated = cleaned[:600]
            last_period = truncated.rfind('.')
            if last_period > 400:  # If there's a sentence end
                cleaned = truncated[:last_period + 1]
            else:
                cleaned = truncated + "..."
        
        return {
            "text": cleaned,
            "subject": result.get('subject', 'Biology'),
            "source_file": result.get('source_file', '9th Class Textbook')
        }
        
    except Exception as e:
        print(f"Search error: {e}")
        return None