import sys
import os
import urllib.parse

# Add parent directory to sys.path
sys.path.append(r"c:\Users\yadav\Downloads\pjt")

def extract_keywords(p):
    filler = {"a", "an", "the", "professional", "shot", "of", "high", "quality", "with", "isolated", "background", "white", "premium", "top", "rated", "view", "photography", "clean", "minimalist"}
    words = [w.strip(",.") for w in p.lower().split() if w.lower().strip(",.") not in filler]
    return ",".join(words[:4])

def test_logic(prod_id, prompt):
    print(f"Testing for ID {prod_id}, Prompt: {prompt[:30]}...")
    keywords = extract_keywords(prompt)
    if len(keywords) < 3:
        keywords += ",product"
    
    seed_val = int(prod_id)
    unique_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(keywords)}?width=1024&height=1024&nologo=true&seed={seed_val}&model=flux"
    print(f"Generated URL: {unique_url}")

test_logic(1, "Nike Running Shoes made of natural wood")
test_logic(28, "Nike Running Shoes made of natural wood")
