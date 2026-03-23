import os
import json
import urllib.parse
from fastapi import HTTPException
import httpx

CACHE_FILE = "../dataset/image_cache.json"

# In-memory dictionary to hold cached URLs
_image_cache = {}

def load_cache():
    global _image_cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                _image_cache = json.load(f)
        except Exception as e:
            print(f"Error loading image cache: {e}")
            _image_cache = {}

def save_cache():
    global _image_cache
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(_image_cache, f, indent=4)

async def get_image_url(product_name: str, description: str):
    """
    Generates a product image URL using Pollinations AI based on name + description.
    Caches the generated URL to dataset/image_cache.json to avoid rate limits/latency.
    """
    cache_key = product_name
    
    if cache_key in _image_cache:
        return _image_cache[cache_key]

    # Clean prompt for image generation
    clean_desc = (description or "")[:100]  # Take first 100 chars to avoid URLs that are too long
    prompt = f"{product_name} {clean_desc} product photography white background ecommerce high quality"
    
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Generate Pollinations AI URL (no auth required)
    # The URL itself is the image, but we can verify it's reachable or just return the URL
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
    
    # Save to Cache
    _image_cache[cache_key] = image_url
    save_cache()
    
    encoded_key = urllib.parse.quote(cache_key)
    return f"http://127.0.0.1:8000/image/{encoded_key}"

# Initialize cache on module load
load_cache()
